# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2024-06-10

### Added
- Complete publications management (CRUD operations)
- Complete certifications management (add, delete)
- Languages section with full CRUD operations
- Badges & achievements section with full CRUD operations
- Skills edit functionality
- All missing template files for all sections
- Document directory auto-creation on CV generation
- Git update script for production deployments

### Fixed
- Duplicate route definitions in cv.py
- CV generation file path issues (absolute paths)
- Nginx configuration (proxy_pass to port instead of socket)
- Docker configuration and permissions
- Missing template errors for all CV sections
- Git ownership issues on production server
- Language form template rendering

### Changed
- Improved error handling for file operations
- Better document directory path handling
- Updated Nginx configuration for better reliability
- Enhanced permission management for production

## [1.1.0] - 2024-05-20

### Added
- Google Analytics 4 tracking
- Cache-control meta tags
- Event tracking for user actions

### Fixed
- Cloudflare caching issues
- Template inheritance problems
- GA tag placement

## [1.0.0] - 2024-05-17

### Added
- Initial release of CV Manager Web
- User registration and authentication
- Profile management
- Work experience, education, and skills sections
- Languages and badges support
- Publication management
- CV generation with multiple templates (Classic, Modern, Compact)
- HTML and PDF export
- Job matching feature
- Responsive dashboard
- CSRF protection
- Database models for all CV sections
- MIT License
- Comprehensive documentation

### Fixed
- CSRF token issues
- Template rendering errors
- Model import issues
- Port conflicts
"
'
