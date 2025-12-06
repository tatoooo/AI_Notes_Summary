#!/bin/bash
uvicorn backend.main:app --reload &
cd frontend && npm run dev &
wait