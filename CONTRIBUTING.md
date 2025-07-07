# Contributing to OCR Labeling Tool

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to the OCR Labeling Tool. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Issue Templates](#issue-templates)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include details about your configuration and environment**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the behavior you expected to see**
- **Explain why this enhancement would be useful**

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these `beginner` and `help-wanted` issues:

- Beginner issues - issues which should only require a few lines of code
- Help wanted issues - issues which should be a bit more involved

## Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/ocr-labeling-tool.git
   cd ocr-labeling-tool
   ```

3. **Set up the backend**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up the frontend**:
   ```bash
   cd frontend
   npm install
   ```

5. **Run the tests**:
   ```bash
   python test_backend.py
   ```

6. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

## Pull Request Process

1. **Update the README.md** with details of changes to the interface, if applicable
2. **Update the requirements.txt** if you add new Python dependencies
3. **Update the frontend/package.json** if you add new Node.js dependencies
4. **Ensure any install or build dependencies are removed** before the end of the layer when doing a build
5. **Test your changes** thoroughly:
   - Run the backend tests: `python test_backend.py`
   - Test the frontend manually
   - Test the OCR functionality with sample images
6. **Update documentation** as needed
7. **Submit your pull request**

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
- [ ] Backend tests pass
- [ ] Frontend functionality tested
- [ ] OCR functionality tested
- [ ] Cross-browser testing (if applicable)

## Checklist:
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def extract_text_from_image(image_path: str) -> Dict[str, Any]:
    """
    Extract text from an image using OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        Dict[str, Any]: Dictionary containing extracted text and metadata
    """
    # Implementation here
    pass
```

### JavaScript/React Code Style

- Use consistent indentation (2 spaces)
- Use meaningful variable and function names
- Use JSDoc comments for complex functions
- Follow React best practices
- Use modern ES6+ features

Example:
```javascript
/**
 * Component for displaying OCR results
 * @param {Object} props - Component props
 * @param {string} props.text - Extracted text
 * @param {Function} props.onSave - Save callback
 */
const OCRResult = ({ text, onSave }) => {
  // Implementation here
};
```

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Good commit messages:
```
Add retry OCR functionality

- Implement retry button in UI
- Add backend endpoint for re-processing images
- Include error handling for failed retries
- Fixes #123
```

## Issue Templates

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.8.5]
- Node.js version: [e.g. 16.14.0]
- Browser: [e.g. Chrome 91]

**Additional context**
Add any other context about the problem here.
```

### Feature Request Template

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## Questions?

Don't hesitate to ask questions by creating an issue with the `question` label.

Thank you for contributing! 🚀 