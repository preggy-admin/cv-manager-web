// Google Analytics Event Tracking for CV Manager

// Track CV generation
function trackCVGeneration(template, format) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'cv_generated', {
            'event_category': 'engagement',
            'event_label': `${template}_${format}`,
            'template': template,
            'format': format
        });
        console.log('Analytics: CV generated -', template, format);
    }
}

// Track job matching
function trackJobMatch(score, jobTitle) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'job_match_performed', {
            'event_category': 'engagement',
            'event_label': jobTitle,
            'value': Math.round(score),
            'match_score': score
        });
        console.log('Analytics: Job match -', score + '%');
    }
}

// Track form submissions
function trackFormSubmission(formName, success) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'form_submission', {
            'event_category': 'conversion',
            'event_label': formName,
            'success': success
        });
        console.log('Analytics: Form submitted -', formName);
    }
}

// Track user registration
function trackRegistration(emailDomain) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'user_registered', {
            'event_category': 'conversion',
            'event_label': emailDomain
        });
        console.log('Analytics: User registered');
    }
}

// Track login
function trackLogin(method) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'user_logged_in', {
            'event_category': 'engagement',
            'event_label': method
        });
        console.log('Analytics: User logged in');
    }
}

// Track section views in CV builder
function trackSectionView(sectionName) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'section_viewed', {
            'event_category': 'engagement',
            'event_label': sectionName
        });
        console.log('Analytics: Section viewed -', sectionName);
    }
}

// Track CV download
function trackCVDownload(format) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'cv_downloaded', {
            'event_category': 'conversion',
            'event_label': format,
            'format': format
        });
        console.log('Analytics: CV downloaded -', format);
    }
}

// Track error occurrences
function trackError(errorType, errorMessage) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'error_occurred', {
            'event_category': 'errors',
            'event_label': errorType,
            'error_message': errorMessage
        });
        console.log('Analytics: Error -', errorType);
    }
}
