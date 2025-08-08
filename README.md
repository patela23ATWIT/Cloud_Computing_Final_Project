# Sporting Shop Management Application

## Group Members
Avi Patel, Jordon Smith, Alex Comeau


## Introduction

Welcome to The Sporting Shop, a growing retail store specializing in sports equipment and apparel. As the business expands, managing inventory, products, vendors, customers, orders, categories, and administrative tasks becomes increasingly more complex. To streamline operations, we have created a Sporting Shop Management Application.


## Description

This project consists of a FastAPI backend service and a Python driver for interactive management. The backend exposes REST API endpoints for all major business management entities, while the driver allows administrators to test and use each endpoint through a simple menu-driven interface. The application connects directly to a MySQL database, ensuring reliable and persistent storage of all store data.

**Key Concepts Demonstrated:**
- REST API development with FastAPI
- Secure admin authentication and session management
- Database connectivity and CRUD operations from Python
- Command-line interface for business management
- Data integrity through foreign key constraints

## Design

The Sporting Shop Management Application is built using FastAPI for the backend and a Python-based driver for interactive management. It interacts using a BFF with a MySQL database that stores all the essential data for the store. Our application provides 10 integrated services to streamline store operations. Vendor, Product, Customer, Order, Inventory, Admin, and Category Management services allow staff to efficiently handle the organization. The Identity Provider ensures secure access for administrators. The BFF (Backend For The Frontend) acts as a secure bridge between the user interface and the backend. Together, these services deliver a reliable and secure platform for managing all aspects of the sporting shop.

### 1. Vendor Management
**Purpose:** Manage the Vendors (companies) that supply products to the store.  
**Features:** Add new vendors, view all vendors, get a vendor by vendor_ID, and remove vendors.  
**Benefit:** Ensures the store always knows who supplies each product and can quickly update supplier information.

### 2. Product Management
**Purpose:** Manage the store’s product catalog.  
**Features:** Add new products, view all products, get product by product_ID, and remove products.  
**Benefit:** Keeps inventory accurate, helps staff quickly find product information, and supports efficient stock management.

### 3. Customer Management
**Purpose:** Manage customer accounts and information.  
**Features:** Add new customers, view all customers, get a customer by customer_id, and remove customers.  
**Benefit:** Enables personalized service and tracks customer orders.

### 4. Order Management
**Purpose:** Track and manage customer orders.  
**Features:** Add new orders, view all orders, get an order by order_id, and remove orders.  
**Benefit:** Ensures timely fulfillment, order history tracking, and accurate shipping and billing.

### 5. Inventory Management
**Purpose:** Monitor and update product stock levels.  
**Features:** Add inventory items, view all inventory, get inventory by product_id, and remove inventory items.  
**Benefit:** Prevents stockouts and overstock, supports purchasing decisions, and maintains accurate inventory records.

### 6. Admin Management
**Purpose:** Manage store administrators and staff accounts.  
**Features:** Add new admins, view all admins, get an admin by admin_id, and remove admins.  
**Benefit:** Controls access to sensitive operations and maintains security.

### 7. Category Management
**Purpose:** Organize products into categories.  
**Features:** Add new categories, view all categories, get a category by category_id, and remove categories.  
**Benefit:** Makes it easier to browse and manage products, and supports reporting by category.

### 8. Identity Provider
**Purpose:** Allow secure sign-ons using admin credentials for login, and passing a cookie or token to verify identity for protected operations.  
**Features:**  
- Allow sign-in and sign-out of the command line driver for security  
- Authenticate admin users against the administrators table  
- Issue a secure session cookie or token upon successful login  
- Allow sign-out to invalidate the session
  
**Benefit:** Ensures only authorized administrators can access management features, protects the application and database from unauthorized access.

### 9. Database
**Purpose:** Store and organize all data for the sporting shop, including products, vendors, customers, orders, inventory, admins, and categories.  
**Features:**  
- MySQL database with tables for each business entity  
- Enforces data integrity with primary and foreign key constraints  
- Supports efficient queries and updates for all management operations  
- Provides a single source for all store data
  
**Benefit:** Ensures data consistency, reliability, and security. Supports all application features and management options.

### 10. BFF (Backend For The Frontend)
**Purpose:** Serve as an intermediary between the frontend (command line driver) and the backend API, handling authentication, session management, and request validation.  
**Features:**  
- Mediates communication between the frontend and the backend  
- Handles authentication and securely manages cookies/tokens  
- Validates requests before passing them to backend services  
- Formats data for frontend consumption
  
**Benefit:** Improves security by adding authentication and session management, simplifies frontend development, and ensures a consistent interface for clients.


## Persistence

The Sporting Shop Management Application uses a persistent MySQL relational database to securely store all business data, including products, vendors, customers, orders, inventory, administrators, and categories. Each entity is represented as a table with well-defined relationships and foreign key constraints to ensure data integrity. All changes made through the application are immediately and reliably saved in the database, providing a consistent record of store operations.


## How to Run the Project

**1. Set Up Your Database**
- Ensure you have MySQL installed and running.
- Import the provided Sporting Shop database schema and sample data (`mysportingshop.sql`).

**2. Install Dependencies**
- Make sure Python 3.8+ is installed.
- Install the required Python packages: `pip install fastapi uvicorn mysql-connector-python httpx`


**3. Configure Database Connection**
- Set your MySQL password as an environment variable (for Windows PowerShell):  `$env:MYSQL_PASSWORD="your_mysql_password"`

**4. Run the FASTAPI Server**
- Open terminal to the project directory, and run: `python main.py` to start up all services. 

**5. Run the Python Driver**
- Open a new terminal to the project directory, and run: `python main_driver.py` to run the driver.

**6. Select and Run a Command Operation** 
- When prompted, select a command number from the menu to perform operations such as viewing, adding, or deleting from our services.

**7. Verify Against the Identity Provider**
- For operations, the user will be prompted to log in with admin credentials. The application will verify your identity using the Identity Provider service before allowing access to features.
- Log in with the default admin credentials: 
- Email: `admin@mysportingshop.com`
- Password: `1234`

**8. Continue Using the Management Application**
- After successful authentication, you can continue to use the management application. As long as your session is valid, you can execute additional commands without re-authenticating, for efficient store management.  
