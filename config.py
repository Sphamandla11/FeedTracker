# config.py

# =============================================================================
# FEEDTRACKER CONFIGURATION FILE
# =============================================================================
# This file contains all the settings, addresses, and translation dictionaries
# needed for the FeedTracker application to communicate with the blockchain.
# It acts as a single source of truth for the app's look, feel, and connection.
# There is no active logic or code execution here — just raw data.
# =============================================================================

# --- NETWORK & CONNECTION ---
# The endpoint used to read data from the Sepolia Testnet without an API key
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

# The public address where the smart contract lives on the Sepolia blockchain
CONTRACT_ADDRESS = "0x4997Ac01cEfe8D78cD7eC64E7d5ef7b3c02BB381"

# --- APPLICATION BRANDING ---
# Text displayed throughout the user interface
APP_NAME = "FeedTracker"
TAGLINE = "Astral Foods Procurement System"
DESCRIPTION = "An end-to-end traceability solution specifically for chicken feed procurement and delivery."

# Path to the local logo file. If this file is missing, the app will gracefully fall back to displaying the APP_NAME text.
LOGO_PATH = "logo.png"

# --- SMART CONTRACT CONSTANTS & TRANSLATIONS ---
# Translating numeric statuses from the blockchain into human-readable English for the interface
FARMER_STATUS_LABELS = {
    0: "Unregistered",
    1: "Application Pending",
    2: "Verified Partner",
    3: "Account Suspended",
    4: "Application Rejected"
}

BATCH_STATUS_LABELS = {
    0: "Freshly Harvested",
    1: "Passed Silo Quality Test",
    2: "Purchase Order Issued",
    3: "Purchase Order Acknowledged",
    4: "Transport Logistics Assigned",
    5: "Transport Job Accepted",
    6: "Loaded onto Transport",
    7: "Currently In Transit",
    8: "Arrived at Destination",
    9: "Delivered & Inspected",
    10: "Final Acceptance (Paid)",
    11: "Rejected / Failed"
}

# --- CONTRACT ABI ---
# The Application Binary Interface (ABI) tells Python exactly what functions exist in the smart contract.
CONTRACT_ABI = [
	
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "acceptTransportJob",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "acknowledgePO",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_reg",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_size",
				"type": "uint256"
			}
		],
		"name": "applyAsFarmer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_transporter",
				"type": "address"
			}
		],
		"name": "assignTransporter",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			}
		],
		"name": "BatchAccepted",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			}
		],
		"name": "BatchDelivered",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			}
		],
		"name": "BatchInTransit",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "confirmArrival",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_crop",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_weight",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_certs",
				"type": "string"
			}
		],
		"name": "createBatch",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "_finalCheck",
				"type": "bool"
			}
		],
		"name": "deliverAndInspect",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "farmer",
				"type": "address"
			}
		],
		"name": "FarmerRegistered",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "farmer",
				"type": "address"
			}
		],
		"name": "FarmerVerified",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			}
		],
		"name": "FeedBatchHarvested",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "finalAcceptance",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_price",
				"type": "uint256"
			}
		],
		"name": "issuePO",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_ticket",
				"type": "string"
			}
		],
		"name": "loadBatch",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "PaymentReleased",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			}
		],
		"name": "PurchaseOrderCreated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			}
		],
		"name": "QualityApproved",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "reason",
				"type": "string"
			}
		],
		"name": "QualityFailed",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_afla",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_moist",
				"type": "uint256"
			}
		],
		"name": "siloQualityCheck",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			}
		],
		"name": "updateToInTransit",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_farmer",
				"type": "address"
			}
		],
		"name": "verifyFarmer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	},
	{
		"inputs": [],
		"name": "admin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "batchCounter",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "batches",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "batchId",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "farmerId",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "transporterId",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "cropType",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "weightKg",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "priceInWei",
				"type": "uint256"
			},
			{
				"internalType": "enum FeedTracker.BatchStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "weighbridgeTicket",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "transportAssignmentTime",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "farmers",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "region",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "farmSize",
				"type": "uint256"
			},
			{
				"internalType": "enum FeedTracker.FarmerStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "certHash",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "MAX_AFLATOXIN_PPB",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "MAX_MOISTURE_PERCENT",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "TRANSPORT_ACCEPT_WINDOW",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}

]
