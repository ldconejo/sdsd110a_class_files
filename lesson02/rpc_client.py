import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:9000/")

result_add = proxy.add(5, 3)
result_sub = proxy.subtract(10, 4)

print("5 +3 =", type(result_add))
print("10 - 4 =", result_sub)
