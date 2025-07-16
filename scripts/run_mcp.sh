#!/bin/bash
export PYTHONPATH=.
uvicorn mcp_server.main:app --reload