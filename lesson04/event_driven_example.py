import asyncio 
# Event-driven task processing 
async def handle_client_request(client_id, request_data):
	print(f"Processing request from client {client_id}") 

	# Simulate I/O operation (database query, file read) 
	await asyncio.sleep(1)  # Non-blocking wait 
	
	result = f"Processed: {request_data}" 
	print(f"Completed request for client {client_id}") 
	return result 

async def server_main(): 
	# Handle multiple clients concurrently 
	clients = [
		handle_client_request(1, "data_A"), 
		handle_client_request(2, "data_B"), 
		handle_client_request(3, "data_C") 
	] 

	# All requests processed concurrently 
	results = await asyncio.gather(*clients) 
	return results 

# Run the event loop 
asyncio.run(server_main())

