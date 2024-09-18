from graphviz import Digraph

# Create a Digraph object
flowchart = Digraph('Cloud and Edge Architecture with Homomorphic Encryption')

# Define nodes for Cloud architecture with homomorphic encryption
flowchart.node('U', 'User/Client')
flowchart.node('HE', 'Homomorphic Encryption Module')
flowchart.node('C', 'Cloud Server')
flowchart.node('R', 'Result Processor')
flowchart.node('D', 'Decryption Module')

# Define nodes for Edge-edge communication
flowchart.node('E1', 'Edge Device 1')
flowchart.node('E2', 'Edge Device 2')

# Define edges for Cloud communication
flowchart.edge('U', 'HE', 'Send Plain Data')
flowchart.edge('HE', 'C', 'Send Encrypted Data')
flowchart.edge('C', 'R', 'Compute on Encrypted Data')
flowchart.edge('R', 'D', 'Send Encrypted Results')
flowchart.edge('D', 'U', 'Decrypt and Get Results')

# Define edges for Edge-edge communication
flowchart.edge('E1', 'HE', 'Encrypt Data at Edge 1')
flowchart.edge('HE', 'E2', 'Send Encrypted Data to Edge 2')
flowchart.edge('E2', 'C', 'Process at Cloud via Edge 2')

# Render the flowchart to file
flowchart.render('cloud_edge_homomorphic_encryption_flowchart', format='png', cleanup=True)

# Display the flowchart
flowchart.view()
