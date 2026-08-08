# Contributing to Hospital LOS Prediction Dashboard

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 How to Contribute

### Reporting Bugs
- Use GitHub Issues to report bugs
- Provide clear description of the problem
- Include reproduction steps
- Mention your Python version and OS

### Suggesting Features
- Check existing issues first
- Create a new issue with detailed description
- Explain the use case and benefits
- Provide example if applicable

### Improving Documentation
- Fix typos and unclear explanations
- Add examples and clarifications
- Improve code comments
- Update outdated information

### Submitting Code
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature: description"`
5. Push to branch: `git push origin feature/my-feature`
6. Open a Pull Request with description

## 📋 Code Guidelines

### Python Style
- Follow PEP 8 style guide
- Use meaningful variable names
- Keep functions small and focused
- Add docstrings to functions

### Comments
- Explain complex logic
- Avoid stating the obvious
- Keep comments up-to-date with code
- Use comments sparingly

### Testing
- Test your changes thoroughly
- Verify all pages load correctly
- Check for performance issues
- Test with different data

## 📝 Commit Messages

Use clear, descriptive commit messages:

```
✨ Add feature: description (for new features)
🐛 Fix bug: description (for bug fixes)
📚 Docs: description (for documentation)
♻️ Refactor: description (for code refactoring)
⚡ Perf: description (for performance improvements)
```

## 🔍 Pull Request Process

1. Update README.md with any new features
2. Add tests or verification steps
3. Ensure CI/CD pipeline passes
4. Request review from maintainers
5. Address review feedback
6. Get approval before merge

## 🎓 Development Setup

```bash
# Clone repository
git clone https://github.com/vimal-kansotia/hospital-los-dashboard.git
cd hospital-los-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Make changes and test
# Commit and push
# Create pull request
```

## 🧪 Testing

Before submitting PR, test:

```bash
# Run linting
flake8 . --max-line-length=100

# Test imports
python -c "import streamlit, pandas, plotly, sklearn"

# Run streamlit (must not error)
streamlit run app.py --logger.level=debug
```

## 📚 Areas for Contribution

### High Priority
- [ ] Add unit tests
- [ ] Improve performance
- [ ] Fix known bugs
- [ ] Enhance documentation

### Medium Priority
- [ ] Add new visualizations
- [ ] Improve UI/UX
- [ ] Add configuration options
- [ ] Optimize database queries

### Nice to Have
- [ ] Add tutorials
- [ ] Create video demos
- [ ] Multilingual support
- [ ] Mobile app version

## 🚫 Code of Conduct

### Be Respectful
- Treat everyone with respect
- Welcome diverse perspectives
- Disagree gracefully
- Give credit where due

### Be Professional
- Keep discussions on-topic
- Avoid spam and self-promotion
- No harassment or discrimination
- Report violations to maintainers

## 📞 Questions?

- Open an issue with your question
- Check existing discussions
- Review documentation
- Ask respectfully and clearly

## 🙏 Thank You!

Your contributions help improve this project for everyone. We appreciate:
- Bug reports
- Feature suggestions
- Code improvements
- Documentation updates
- Positive feedback

---

**Happy Contributing!** 🎉

For questions about this CONTRIBUTING.md, open an issue or contact the maintainers.
