# Contributing to Harv v2.0

Thank you for your interest in contributing to the Harv v2.0 Intelligent Tutoring System!

## Development Setup

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/harv-v2.git
   cd harv-v2
   ```

3. **Set up development environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## Code Standards

- **Python**: Follow PEP 8
- **Type Hints**: Required for all functions
- **Documentation**: Docstrings for all public methods
- **Testing**: Unit tests for new features

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation
6. Submit pull request

## Code Review Criteria

- Code follows established patterns
- Tests cover new functionality
- Documentation is updated
- No breaking changes without discussion
- Performance impact considered

## Feature Requests

Open an issue with:
- Clear description of the problem
- Proposed solution
- Use cases and benefits
- Implementation considerations
