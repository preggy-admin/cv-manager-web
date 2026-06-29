"""
Bulk import utilities for CV sections.
Supports CSV and JSON formats for: publications, skills, work experience, education.
"""

import csv
import json
import io
from app import db
from app.models import Publication, Skill, WorkExperience, Education


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def _parse_csv(file_stream):
    """Parse a CSV file stream into a list of dicts."""
    text = file_stream.read().decode('utf-8', errors='replace')
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


def _parse_json(file_stream):
    """Parse a JSON file stream into a list of dicts."""
    data = json.loads(file_stream.read().decode('utf-8'))
    if isinstance(data, list):
        return data
    raise ValueError("JSON must be a top-level array of objects.")


def _parse_file(file_storage, fmt):
    """Dispatch to CSV or JSON parser based on fmt ('csv' | 'json')."""
    if fmt == 'csv':
        return _parse_csv(file_storage.stream)
    elif fmt == 'json':
        return _parse_json(file_storage.stream)
    raise ValueError(f"Unsupported format: {fmt}")


# ---------------------------------------------------------------------------
# Publications importer
# Expected CSV columns: title, authors, year, journal, conference,
#                       publisher, doi, pages, volume, issue, pub_type
# ---------------------------------------------------------------------------

def import_publications(user_id, file_storage, fmt='csv'):
    """Import publications for a user. Skips entries with duplicate DOI (if present)."""
    rows = _parse_file(file_storage, fmt)
    inserted, skipped, errors = 0, 0, []

    existing_dois = {
        p.doi for p in Publication.query.filter_by(user_id=user_id).all() if p.doi
    }
    existing_titles = {
        p.title.lower() for p in Publication.query.filter_by(user_id=user_id).all()
    }
    order_start = Publication.query.filter_by(user_id=user_id).count()

    for i, row in enumerate(rows):
        try:
            title = (row.get('title') or '').strip()
            doi = (row.get('doi') or '').strip() or None

            if not title:
                errors.append(f"Row {i+1}: missing title — skipped.")
                skipped += 1
                continue

            if doi and doi in existing_dois:
                skipped += 1
                continue
            if not doi and title.lower() in existing_titles:
                skipped += 1
                continue

            pub = Publication(
                user_id=user_id,
                title=title,
                authors=row.get('authors', '').strip(),
                year=row.get('year', '').strip(),
                journal=row.get('journal', '').strip(),
                conference=row.get('conference', '').strip(),
                publisher=row.get('publisher', '').strip(),
                doi=doi,
                pages=row.get('pages', '').strip(),
                volume=row.get('volume', '').strip(),
                issue=row.get('issue', '').strip(),
                pub_type=row.get('pub_type', 'article').strip(),
                order=order_start + inserted,
            )
            db.session.add(pub)
            existing_dois.add(doi or '')
            existing_titles.add(title.lower())
            inserted += 1
        except Exception as e:
            errors.append(f"Row {i+1}: {e}")

    db.session.commit()
    return inserted, skipped, errors


# ---------------------------------------------------------------------------
# Skills importer
# Expected CSV columns: name, category, proficiency (1-5)
# ---------------------------------------------------------------------------

def import_skills(user_id, file_storage, fmt='csv'):
    """Import skills for a user. Skips duplicate name+category pairs."""
    rows = _parse_file(file_storage, fmt)
    inserted, skipped, errors = 0, 0, []

    existing = {
        (s.name.lower(), (s.category or '').lower())
        for s in Skill.query.filter_by(user_id=user_id).all()
    }
    order_start = Skill.query.filter_by(user_id=user_id).count()

    for i, row in enumerate(rows):
        try:
            name = (row.get('name') or '').strip()
            category = (row.get('category') or '').strip()

            if not name:
                errors.append(f"Row {i+1}: missing name — skipped.")
                skipped += 1
                continue

            key = (name.lower(), category.lower())
            if key in existing:
                skipped += 1
                continue

            proficiency = int(row.get('proficiency', 3))
            proficiency = max(1, min(5, proficiency))

            skill = Skill(
                user_id=user_id,
                name=name,
                category=category,
                proficiency=proficiency,
                order=order_start + inserted,
            )
            db.session.add(skill)
            existing.add(key)
            inserted += 1
        except Exception as e:
            errors.append(f"Row {i+1}: {e}")

    db.session.commit()
    return inserted, skipped, errors


# ---------------------------------------------------------------------------
# Work Experience importer
# Expected CSV columns: company, position, start_date, end_date, description, current
# ---------------------------------------------------------------------------

def import_experience(user_id, file_storage, fmt='csv'):
    """Import work experience entries for a user."""
    rows = _parse_file(file_storage, fmt)
    inserted, skipped, errors = 0, 0, []

    existing = {
        (e.company.lower(), e.position.lower())
        for e in WorkExperience.query.filter_by(user_id=user_id).all()
    }
    order_start = WorkExperience.query.filter_by(user_id=user_id).count()

    for i, row in enumerate(rows):
        try:
            company = (row.get('company') or '').strip()
            position = (row.get('position') or '').strip()

            if not company or not position:
                errors.append(f"Row {i+1}: missing company or position — skipped.")
                skipped += 1
                continue

            key = (company.lower(), position.lower())
            if key in existing:
                skipped += 1
                continue

            current_val = str(row.get('current', 'false')).lower() in ('true', '1', 'yes')
            exp = WorkExperience(
                user_id=user_id,
                company=company,
                position=position,
                start_date=row.get('start_date', '').strip(),
                end_date=row.get('end_date', '').strip(),
                current=current_val,
                description=row.get('description', '').strip(),
                order=order_start + inserted,
            )
            db.session.add(exp)
            existing.add(key)
            inserted += 1
        except Exception as e:
            errors.append(f"Row {i+1}: {e}")

    db.session.commit()
    return inserted, skipped, errors


# ---------------------------------------------------------------------------
# Education importer
# Expected CSV columns: institution, degree, field, start_year, end_year, description
# ---------------------------------------------------------------------------

def import_education(user_id, file_storage, fmt='csv'):
    """Import education entries for a user."""
    rows = _parse_file(file_storage, fmt)
    inserted, skipped, errors = 0, 0, []

    existing = {
        (e.institution.lower(), e.degree.lower())
        for e in Education.query.filter_by(user_id=user_id).all()
    }
    order_start = Education.query.filter_by(user_id=user_id).count()

    for i, row in enumerate(rows):
        try:
            institution = (row.get('institution') or '').strip()
            degree = (row.get('degree') or '').strip()

            if not institution or not degree:
                errors.append(f"Row {i+1}: missing institution or degree — skipped.")
                skipped += 1
                continue

            key = (institution.lower(), degree.lower())
            if key in existing:
                skipped += 1
                continue

            edu = Education(
                user_id=user_id,
                institution=institution,
                degree=degree,
                field=row.get('field', '').strip(),
                start_year=row.get('start_year', '').strip(),
                end_year=row.get('end_year', '').strip(),
                description=row.get('description', '').strip(),
                order=order_start + inserted,
            )
            db.session.add(edu)
            existing.add(key)
            inserted += 1
        except Exception as e:
            errors.append(f"Row {i+1}: {e}")

    db.session.commit()
    return inserted, skipped, errors


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

IMPORTERS = {
    'publications': import_publications,
    'skills': import_skills,
    'experience': import_experience,
    'education': import_education,
}


def run_import(section, user_id, file_storage, fmt='csv'):
    """Dispatch to the correct importer by section name."""
    if section not in IMPORTERS:
        raise ValueError(f"Unknown section: {section}. Choose from: {list(IMPORTERS)}")
    return IMPORTERS[section](user_id, file_storage, fmt)
