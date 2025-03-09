# Log Analysis AI Agent with MITRE ATT&CK Framework Integration

A powerful security log analysis tool that uses n8n workflows and OpenAI to automatically detect suspicious activities in log files and map them to the MITRE ATT&CK framework.

## Features

- **Automated Log Analysis**: Parse and analyze log files to identify suspicious patterns
- **MITRE ATT&CK Mapping**: Automatically map detected threats to MITRE ATT&CK tactics and techniques
- **AI-Powered Analysis**: Use OpenAI's GPT models to generate human-readable security reports
- **Comprehensive Reporting**: Generate detailed HTML reports with statistics and findings
- **Easy to Use**: Simple command-line interface for uploading and analyzing logs

## Requirements

- Node.js v18.17.0 or later (v20 and v22 are also supported)
- n8n (v1.64.0+)
- Python 3.6+
- OpenAI API Key

## Installation

### 1. Install n8n

```bash
npm install n8n -g
```

If you experience version compatibility issues, consider using nvm:

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Install compatible Node.js version
nvm install 18.17.0
nvm use 18.17.0

# Install n8n
npm install n8n -g
```

### 2. Clone this repository

```bash
git clone https://github.com/yourusername/log-analysis-ai-agent.git
cd log-analysis-ai-agent
```

### 3. Set up the n8n workflow

```bash
# Start n8n
n8n start

# Import the workflow
# Open http://localhost:5678 in your browser and import n8n-log-analyzer.json
```

### 4. Configure OpenAI API Key

1. In the n8n interface, open the imported workflow
2. Click on the OpenAI node
3. Configure the OpenAI API integration with your API key
4. Save the workflow

### 5. Install Python dependencies

```bash
pip install requests
```

## Usage

### Analyzing Log Files

Use the provided Python script to analyze log files:

```bash
./log-upload-script.py your-logfile.log --webhook http://localhost:5678/webhook/receive-logs
```

Alternatively, you can use curl or wget:

```bash
# Using curl
curl -X POST -H "Content-Type: text/plain" --data-binary @your-logfile.log http://localhost:5678/webhook/receive-logs

# Using wget
wget --post-file=your-logfile.log --header="Content-Type: text/plain" -O response.json http://localhost:5678/webhook/receive-logs
```

### Output

The tool provides:

1. **Terminal Summary**: Basic statistics about the log analysis
2. **HTML Report**: Detailed report with findings, statistics, and AI analysis
3. **JSON Response**: Full analysis data in JSON format

## Workflow Architecture

The log analysis workflow consists of several n8n nodes:

1. **Webhook**: Receives the log file via HTTP POST
2. **File Parser**: Extracts log entries and formats them for processing
3. **Log Processor**: Analyzes log entries to identify patterns and extract metadata
4. **Abnormal Detector**: Identifies suspicious activities and maps them to MITRE ATT&CK
5. **OpenAI**: Generates a human-readable security analysis
6. **Report Generator**: Creates comprehensive HTML and JSON reports
7. **Respond to Webhook**: Returns the analysis results

## Customization

### Adding Custom Detection Patterns

Edit the Abnormal Detector node to add your own detection patterns:

```javascript
const abnormalPatterns = [
  // Add your patterns here
  { 
    pattern: /your-regex-pattern/, 
    category: 'Custom Category', 
    mitreTactic: 'TA00XX', 
    mitreTechnique: 'T10XX' 
  },
  // ...
];
```

### Modifying Log Format Parsing

If your log format differs from the default, modify the Log Processor node:

```javascript
// Adjust regex patterns to match your log format
const timestampMatch = line.match(/your-timestamp-pattern/);
const levelMatch = line.match(/your-level-pattern/);
const componentMatch = line.match(/your-component-pattern/);
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [n8n](https://n8n.io/) for the powerful workflow automation platform
- [OpenAI](https://openai.com/) for the AI analysis capabilities
- [MITRE ATT&CK](https://attack.mitre.org/) for the cybersecurity framework
