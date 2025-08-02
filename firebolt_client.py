"""Convenience wrapper around the Firebolt Python SDK.

This module exposes a singleton connection as ``conn`` and small helper
functions for running queries.  It also ensures—as a best-effort—that the
three core SynapseTrader tables exist:
  • trades         – booked trades / executions
  • market_snaps   – spot & yields used for pricing
  • audit          – any compliance-relevant event in JSON form

Environment variables required (see .env.template):
  FIREBOLT_ACCOUNT          # e.g. 'myaccount'
  FIREBOLT_DATABASE         # 'synapse_trader'
  FIREBOLT_ENGINE           # name of provisioned compute engine
  FIREBOLT_USERNAME
  FIREBOLT_PASSWORD

The first import of this module is idempotent and cheap; subsequent imports
reuse the open connection.
"""
from __future__ import annotations

import os
from typing import Any, Iterable, Sequence

from dotenv import load_dotenv
from firebolt.db import connect
from firebolt.db.connection import Connection
from firebolt.db.cursor import Cursor

load_dotenv()

# ---------------------------------------------------------------------------
# Establish connection (lazy) ------------------------------------------------
# ---------------------------------------------------------------------------

def _create_connection() -> Connection:
    return connect(
        auth=ClientCredentials(
        os.getenv("FIREBOLT_CLIENT_ID"),
        os.getenv("FIREBOLT_CLIENT_SECRET")
    ),
    engine_name=os.getenv('FIREBOLT_ENGINE'),
    database=os.getenv('FIREBOLT_DB'),
    account_name=os.getenv('FIREBOLT_ACCOUNT'),
    )


conn: Connection | None = None


def get_conn() -> Connection:  # public accessor
    global conn
    if conn is None:
        conn = _create_connection()
        _create_schema(conn)
    return conn


# ---------------------------------------------------------------------------
# Schema bootstrap -----------------------------------------------------------
# ---------------------------------------------------------------------------

def _execute_ddl(cur: Cursor, ddl: str) -> None:
    try:
        cur.execute(ddl)
    except Exception as exc:  # noqa: BLE001 – Firebolt raises generic
        # If table already exists, ignore
        if "already exists" not in str(exc).lower():
            raise


def _create_schema(connection: Connection) -> None:
    ddl_statements: Sequence[str] = (
        """
        CREATE FACT TABLE IF NOT EXISTS trades (
            tx_id TEXT,
            client_id TEXT,
            ccy_pair TEXT,
            notional_usd DOUBLE,
            tenor TEXT,
            fwd_points DOUBLE,
            price DOUBLE,
            side TEXT,
            booked_at TIMESTAMP
        ) PRIMARY INDEX tx_id;
        """,
        """
        CREATE FACT TABLE IF NOT EXISTS market_snaps (
            ts TIMESTAMP,
            pair TEXT,
            spot DOUBLE,
            usd_3m DOUBLE,
            gbp_3m DOUBLE
        ) PRIMARY INDEX (ts, pair);
        """,
        """
        CREATE FACT TABLE IF NOT EXISTS audit (
            ts TIMESTAMP,
            event_type TEXT,
            payload TEXT
        ) PRIMARY INDEX ts;
        """,
    )

    cur = connection.cursor()
    for ddl in ddl_statements:
        _execute_ddl(cur, ddl)
    cur.close()


# ---------------------------------------------------------------------------
# Helper functions -----------------------------------------------------------
# ---------------------------------------------------------------------------

def execute(query: str, params: Iterable[Any] | None = None) -> None:
    """Execute a statement without returning rows."""
    cur = get_conn().cursor()
    cur.execute(query, params or [])
    cur.close()


def fetchall(query: str, params: Iterable[Any] | None = None):
    cur = get_conn().cursor()
    cur.execute(query, params or [])
    rows = cur.fetchall()
    cur.close()
    return rows
