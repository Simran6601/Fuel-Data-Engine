# FuelData Engine

## Overview

FuelData Engine is a Django-based fleet route optimization platform that calculates the most cost-effective fuel stops for long-distance trips across the United States.

The system generates driving routes using the OSRM routing engine, identifies optimal fuel stations along the route using fuel price data, estimates total fuel costs, and recommends alternative stations when available.

This project was developed as part of a Backend Django Engineer technical assessment.

---

# Features

### Route Planning

* Route generation between any two US locations
* Powered by OSRM (Open Source Routing Machine)
* Distance and travel time estimation

### Fuel Optimization

* Assumes vehicle range of 500 miles
* Automatically determines required fuel stops
* Recommends lowest-cost fuel stations near route checkpoints
* Provides alternative fuel station recommendations

### Cost Estimation

* Vehicle fuel efficiency: 10 MPG
* Calculates fuel required for the entire trip
* Estimates total fuel cost
* Calculates estimated savings compared to worst-case fuel pricing

### Analytics

* Fuel station statistics
* Cheapest states by average fuel price
* Most expensive states by average fuel price

### Developer Features

* Django REST Framework APIs
* Swagger/OpenAPI Documentation
* Django Admin Dashboard
* Automated Test Suite
* API Response Caching
* Performance Optimizations

---

# Technology Stack

| Component      | Technology                |
| -------------- | ------------------------- |
| Backend        | Django 6                  |
| API Framework  | Django REST Framework     |
| Documentation  | DRF Spectacular           |
| Routing Engine | OSRM                      |
| Database       | SQLite                    |
| Testing        | Django Test Framework     |
| Caching        | Django Local Memory Cache |

---

# Architecture

User Request

↓

Route Planner API

↓

Geocoding

↓

OSRM Route Generation

↓

Route Checkpoint Generation

↓

Fuel Station Optimization

↓

Cost Calculation

↓

JSON Response

---

# Assumptions

The application uses the following assumptions:

| Parameter               | Value     |
| ----------------------- | --------- |
| Vehicle Range           | 500 Miles |
| Vehicle Efficiency      | 10 MPG    |
| Fuel Stop Search Radius | 100 Miles |
| Route Engine            | OSRM      |

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd FuelData-Engine
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
python manage.py migrate
```

## Start Server

```bash
python manage.py runserver
```

---

# API Documentation

Swagger UI:

```text
/api/docs/
```

OpenAPI Schema:

```text
/api/schema/
```

---

# Available Endpoints

## Health Check

```http
GET /api/health/
```

Response:

```json
{
  "status": "healthy",
  "service": "FuelData Engine"
}
```

---

## Route Planner

```http
GET /api/route-planner/?start=Dallas,TX&end=Chicago,IL
```

Response:

```json
{
  "distance_miles": 966.45,
  "estimated_drive_hours": 17.09,
  "fuel_needed": 96.65,
  "estimated_cost": 338.16
}
```

---

## Fuel Stations

```http
GET /api/fuel-stations/
```

---

## Station Statistics

```http
GET /api/station-stats/
```

---

## Cheapest States

```http
GET /api/cheapest-states/
```

---

## Most Expensive States

```http
GET /api/most-expensive-states/
```

---

## Route Cost Calculator

```http
GET /api/route-cost/
```

---

## Route Optimizer

```http
GET /api/route-optimizer/
```

---

# Performance Optimizations

### Response Caching

Route planning responses are cached for one hour to reduce repeated routing API requests and improve response times.

### Fuel Station Filtering

Fuel stations are filtered using geographic bounding-box searches before distance calculations are performed.

### Database Indexes

Indexes are created on:

* State
* City
* Retail Price

to improve query performance.

---

# Testing

Run all tests:

```bash
python manage.py test
```

Current Test Coverage Includes:

* Health Check Endpoint
* Route Cost Validation
* Route Optimizer Validation
* Fuel Station Pagination
* Cheapest Stations
* Cheapest States
* State Prices
* Route Planner Validation
* Station Statistics

Result:

```text
Found 15 test(s)
Ran 15 tests

OK
```

---

# Admin Dashboard

Django Admin is available at:

```text
/admin/
```

Features:

* Fuel Station Management
* Search and Filtering
* Fuel Price Analytics
* Pagination
* Sorting

---

# Future Improvements

* PostgreSQL + PostGIS Integration
* Redis Caching
* JWT Authentication
* Route History Storage
* Real-Time Fuel Price Updates
* Interactive Route Maps
* Docker Deployment

---

# Author

Simran Jamadar

Backend Django Engineer Assessment Project

2026











