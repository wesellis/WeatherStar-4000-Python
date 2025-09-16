# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in WeatherStar 4000 Python, please report it by:

1. **Do not** create a public issue
2. Send details to the repository owner via GitHub private message
3. Include steps to reproduce if possible

## Security Updates

This project uses the following dependencies with regular security updates:

- **pygame**: 2.6.0+ (display rendering)
- **requests**: 2.32.3+ (API calls)
- **Pillow**: 10.4.0+ (image processing)

All dependencies are kept up-to-date to address known vulnerabilities.

## Best Practices

- Never commit API keys or sensitive data
- Use environment variables for configuration
- Keep dependencies updated regularly
- Review third-party code before including it