from banking.audit import log_action

print("Starting audit test...")

result = log_action(
    "ACC329300",
    "TEST_ACTION",
    "Testing PyBank audit log"
)

print("Result:", result)