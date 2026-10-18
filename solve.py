import json

# 1. PASTE YOUR CAPTURED BYTE CHUNKS HERE
data = {
  "A": [
    "7b22726573706f6e736522",
    "3a225265706f7274206a6f622d36623635653264633a",
    "20222c22646f6e65223a66616c73657d0a7b",
    "227468696e6b696e67223a22696e7465726e616c206e6f",
    "7465222c22726573706f6e7365223a22222c2264",
    "6f6e65223a66616c73657d0a7b22",
    "726573706f6e7365223a22636166c3",
    "a95c6e222c22646f6e65223a66616c7365",
    "7d0a7b22726573706f6e7365223a22526561647920",
    "e2",
    "9c93222c22646f6e65223a747275652c22",
    "646f6e655f726561736f6e223a2273746f70227d0a"
  ],
  "B": [
    "7b22726573706f6e736522",
    "3a225061727469616c206a6f622d3662363565326463",
    "222c22646f6e65223a66616c73657d0a7b22",
    "726573706f6e7365223a22756e66696e6973686564"
  ],
  "C": [
    "7b22726573706f6e736522",
    "3a224472616674206a6f622d3662363565326463222c",
    "22646f6e65223a66616c73657d0a7b226572",
    "726f72223a226d6f64656c20756e6c6f61646564227d0a",
    "7b22726573706f6e7365223a2249474e4f524522",
    "2c22646f6e65223a747275657d0a"
  ]
}

result = {}
for key, chunks in data.items():
    # Combine hex BEFORE decoding to safely preserve multi-byte UTF-8 characters across boundaries
    raw_bytes = bytes.fromhex("".join(chunks))
    text = raw_bytes.decode('utf-8')
    
    full_response = ""
    complete = False
    error_msg = None
    
    # Process newline-delimited JSON records[cite: 81]
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            # EOF without terminal record (incomplete trailing JSON)[cite: 81]
            break
            
        if "error" in record and record["error"] is not None:
            error_msg = record["error"]
            complete = False
            break
            
        if "response" in record:
            full_response += record["response"]
            
        if record.get("done") is True:
            complete = True
            break
            
    result[key] = {
        "text": full_response,
        "complete": complete,
        "error": error_msg
    }

with open("answer.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)

print("Success! answer.json has been created.")
