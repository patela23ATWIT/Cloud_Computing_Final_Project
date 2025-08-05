from api.types import *
from api.utils import spin_up_fastapi_service


VENDOR_PORT = 8000
INVENTORY_PORT = 8001
PRODUCTS_PORT = 8002
CUSTOMERS_PORT = 8003
ORDERS_PORT = 8004
ADMINS_PORT = 8005
CATEGORIES_PORT = 8006


def print_service_output(line):
    print(line, end="")



if __name__ == "__main__":
    # Spin up the cookies service on port 9000
    spin_up_fastapi_service("api.services.cookies", port=8007, stdout_callback=print_service_output)

    # Spin up other services
    spin_up_fastapi_service("api.services.vendors", port=VENDOR_PORT, stdout_callback=print_service_output)
    spin_up_fastapi_service("api.services.inventory", port=INVENTORY_PORT, stdout_callback=print_service_output)
    spin_up_fastapi_service("api.services.products", port=PRODUCTS_PORT, stdout_callback=print_service_output)
    spin_up_fastapi_service("api.services.customers", port=CUSTOMERS_PORT, stdout_callback=print_service_output)
    spin_up_fastapi_service("api.services.orders", port=ORDERS_PORT, stdout_callback=print_service_output)
    spin_up_fastapi_service("api.services.admins", port=ADMINS_PORT, stdout_callback=print_service_output)
    spin_up_fastapi_service("api.services.categories", port=CATEGORIES_PORT, stdout_callback=print_service_output)

    # Keep the main thread alive
    try:
        print("All services started. Press Ctrl+C to stop.")
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down services.")


