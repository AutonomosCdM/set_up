# Contributing to Google Workspace Intelligent Agent

## Welcome Contributors!

We're thrilled that you're interested in contributing to the Google Workspace Intelligent Agent project. This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others. Harassment, discrimination, and offensive behavior are not tolerated.

## How to Contribute

### Reporting Bugs

1. Check existing issues to ensure the bug hasn't been reported
2. Use the issue template to provide detailed information
3. Include steps to reproduce, expected behavior, and actual behavior

### Suggesting Enhancements

1. Check existing issues and discussions
2. Provide clear and detailed explanation of the suggestion
3. Include potential implementation ideas if possible

### Pull Requests

#### Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests and code quality checks
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

#### Pull Request Guidelines

- Provide a clear description of your changes
- Link to any related issues
- Ensure all tests pass
- Follow the project's coding standards

## Development Setup

### Prerequisites

- Python 3.9+
- Poetry
- Google Cloud Project credentials
- Groq API Key

### Installation

```bash
# Clone your fork
git clone https://github.com/your-username/google-workspace-agent.git
cd google-workspace-agent

# Install dependencies
poetry install
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test suite
poetry run pytest tests/test_gmail_client.py

# Code quality checks
poetry run mypy src
poetry run black --check src
poetry run flake8 src
```

## Contribution Areas

We welcome contributions in various areas:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Test coverage
- Performance optimizations
- New service integrations

## Code Standards

- Follow PEP 8 style guidelines
- Write clear, concise comments
- Maintain type hints
- Write comprehensive tests for new features
- Ensure backward compatibility

## Reporting Security Issues

If you discover a security vulnerability, please send an email to [security@example.com] instead of creating a public issue.

## Questions?

If you have any questions, feel free to:
- Open an issue
- Ask on our discussion forum
- Reach out to project maintainers

## Thank You!

Your contributions make this project better for everyone. We appreciate your help!
