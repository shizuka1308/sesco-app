def main():
    try:
        client = establish_clickhouse_connection()
        create_reactor_status_table(client)
        download_and_insert_data(client)
        print("Data processing and insertion completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if client:
            client.disconnect()

if __name__ == "__main__":
    main()