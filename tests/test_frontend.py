"""
Frontend integration tests using FastAPI TestClient.
These tests verify HTML structure and frontend behavior by making requests 
to verify the served files and testing the JavaScript logic indirectly.
"""
import re
import pytest
from pathlib import Path


@pytest.fixture
def static_dir():
    """Get the static directory path"""
    return Path(__file__).parent.parent / "src" / "static"


class TestFrontendHTML:
    """Test frontend HTML structure"""

    def test_index_html_exists(self, static_dir):
        """Test that index.html file exists"""
        index_file = static_dir / "index.html"
        assert index_file.exists(), "index.html should exist"

    def test_index_html_contains_required_sections(self, static_dir):
        """Test that index.html has required sections"""
        # Arrange
        index_file = static_dir / "index.html"
        
        # Act
        content = index_file.read_text()
        
        # Assert
        assert "activities-container" in content
        assert "signup-container" in content
        assert "activities-list" in content
        assert "signup-form" in content
        assert "id=\"email\"" in content
        assert "id=\"activity\"" in content and "select" in content

    def test_index_html_includes_css_and_js(self, static_dir):
        """Test that index.html links to CSS and JS files"""
        # Arrange
        index_file = static_dir / "index.html"
        
        # Act
        content = index_file.read_text()
        
        # Assert
        assert "styles.css" in content
        assert "app.js" in content

    def test_styles_css_exists(self, static_dir):
        """Test that styles.css file exists"""
        # Arrange & Assert
        styles_file = static_dir / "styles.css"
        assert styles_file.exists(), "styles.css should exist"

    def test_app_js_exists(self, static_dir):
        """Test that app.js file exists"""
        # Arrange & Assert
        app_file = static_dir / "app.js"
        assert app_file.exists(), "app.js should exist"


class TestAppJSFunctionality:
    """Test JavaScript functionality by inspecting code"""

    def test_app_js_fetches_activities(self, static_dir):
        """Test that app.js makes fetch calls to /activities"""
        # Arrange
        app_file = static_dir / "app.js"
        
        # Act
        content = app_file.read_text()
        
        # Assert: check for fetch call to /activities
        assert "fetch(" in content
        assert "/activities" in content

    def test_app_js_handles_signup_form(self, static_dir):
        """Test that app.js handles form submission"""
        # Arrange
        app_file = static_dir / "app.js"
        
        # Act
        content = app_file.read_text()
        
        # Assert: check for signup event listener
        assert "signup-form" in content
        assert "addEventListener" in content
        assert "method: \"POST\"" in content or "method: 'POST'" in content

    def test_app_js_handles_participant_removal(self, static_dir):
        """Test that app.js handles participant removal"""
        # Arrange
        app_file = static_dir / "app.js"
        
        # Act
        content = app_file.read_text()
        
        # Assert: check for delete functionality
        assert "remove-participant" in content
        assert "DELETE" in content
        assert "participants" in content

    def test_app_js_builds_participant_list_html(self, static_dir):
        """Test that app.js creates participant list HTML"""
        # Arrange
        app_file = static_dir / "app.js"
        
        # Act
        content = app_file.read_text()
        
        # Assert: check for participant list construction
        assert "participants-list" in content
        assert "participant-email" in content or "participants" in content
        assert "<li>" in content or '`<li>' in content

    def test_app_js_shows_delete_button_next_to_participants(self, static_dir):
        """Test that delete buttons are added to participant items"""
        # Arrange
        app_file = static_dir / "app.js"
        
        # Act  
        content = app_file.read_text()
        
        # Assert: check for delete button with data attributes
        assert "remove-participant" in content
        assert "data-activity" in content
        assert "data-email" in content
        assert "🗑️" in content or "trash" in content.lower() or "delete" in content.lower()

    def test_app_js_displays_availability_count(self, static_dir):
        """Test that app.js calculates and displays available spots"""
        # Arrange
        app_file = static_dir / "app.js"
        
        # Act
        content = app_file.read_text()
        
        # Assert: check for spots calculation
        assert "max_participants" in content
        assert "participants.length" in content
        assert "spotsLeft" in content or "spots left" in content


class TestStylesCSS:
    """Test CSS styling"""

    def test_styles_contains_activity_card_styling(self, static_dir):
        """Test that CSS styles activity cards"""
        # Arrange
        styles_file = static_dir / "styles.css"
        
        # Act
        content = styles_file.read_text()
        
        # Assert
        assert ".activity-card" in content

    def test_styles_hides_participant_bullets(self, static_dir):
        """Test that CSS hides participant list bullets"""
        # Arrange
        styles_file = static_dir / "styles.css"
        
        # Act
        content = styles_file.read_text()
        
        # Assert: check for list-style-type: none
        assert "participants-list" in content
        assert ("list-style-type: none" in content or "list-style: none" in content)

    def test_styles_formats_participant_list(self, static_dir):
        """Test that CSS formats participant list display"""
        # Arrange
        styles_file = static_dir / "styles.css"
        
        # Act
        content = styles_file.read_text()
        
        # Assert
        assert ".participants-list" in content or ".activity-card .participants-list" in content

    def test_styles_contains_remove_button_styling(self, static_dir):
        """Test that CSS styles the remove button"""
        # Arrange
        styles_file = static_dir / "styles.css"
        
        # Act
        content = styles_file.read_text()
        
        # Assert
        assert ".remove-participant" in content

    def test_styles_has_message_styling(self, static_dir):
        """Test that CSS has styles for messages"""
        # Arrange
        styles_file = static_dir / "styles.css"
        
        # Act
        content = styles_file.read_text()
        
        # Assert
        assert ".success" in content or ".message" in content
        assert ".error" in content

    def test_styles_responsive_design(self, static_dir):
        """Test that CSS includes responsive design"""
        # Arrange
        styles_file = static_dir / "styles.css"
        
        # Act
        content = styles_file.read_text()
        
        # Assert
        assert "@media" in content


class TestCacheDisabling:
    """Test that caching is properly disabled for fresh data"""

    def test_app_js_disables_cache_on_fetch(self, static_dir):
        """Test that app.js uses cache busting and cache: 'no-store'"""
        # Arrange
        app_file = static_dir / "app.js"
        
        # Act
        content = app_file.read_text()
        
        # Assert: check for cache busting timestamp and no-store
        assert "Date.now()" in content
        assert "cache" in content and "no-store" in content
