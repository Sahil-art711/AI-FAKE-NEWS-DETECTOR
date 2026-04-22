// =============================================================
// script.js — Event Management Website | Experiment 4
// Student Name  : Sahil Jha
// Roll Number   : 2401010157
// Date          : 2026-05-04
// Description   : Client-side interactivity — form validation,
//                 live search, mobile navigation toggle,
//                 and flash message auto-dismiss.
// =============================================================

"use strict";

/* ── Mobile Navigation Toggle ── */
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("navToggle");
  const links  = document.getElementById("navLinks");

  if (toggle && links) {
    toggle.addEventListener("click", () => {
      links.classList.toggle("open");
      // Animate hamburger → X
      const spans = toggle.querySelectorAll("span");
      toggle.classList.toggle("active");
    });

    // Close menu when a link is clicked
    links.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => links.classList.remove("open"));
    });
  }

  /* ── Auto-dismiss Flash Messages ── */
  setTimeout(() => {
    document.querySelectorAll(".flash").forEach(el => {
      el.style.transition = "opacity .5s";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    });
  }, 5000);
});


/* ── Registration Form Validation ── */
const registrationForm = document.getElementById("registrationForm");

if (registrationForm) {
  registrationForm.addEventListener("submit", function (e) {
    e.preventDefault();   // Prevent default before validating
    if (validateForm()) {
      this.submit();
    }
  });

  // Real-time validation feedback
  ["name", "email", "phone", "event_id", "tickets"].forEach(fieldId => {
    const el = document.getElementById(fieldId);
    if (el) {
      el.addEventListener("blur",  () => validateField(fieldId));
      el.addEventListener("input", () => clearError(fieldId));
    }
  });
}

/**
 * Validate all form fields. Returns true if all are valid.
 */
function validateForm() {
  const fields = ["name", "email", "phone", "event_id", "tickets"];
  let valid = true;
  fields.forEach(id => { if (!validateField(id)) valid = false; });
  return valid;
}

/**
 * Validate a single field by its ID.
 * @param {string} fieldId
 * @returns {boolean}
 */
function validateField(fieldId) {
  const el    = document.getElementById(fieldId);
  const error = document.getElementById(fieldId + "Error");
  if (!el || !error) return true;

  const value = el.value.trim();

  // Clear previous error
  clearError(fieldId);

  switch (fieldId) {

    case "name":
      if (!value) {
        return showError(fieldId, "Full name is required.");
      }
      if (value.length < 3) {
        return showError(fieldId, "Name must be at least 3 characters.");
      }
      break;

    case "email":
      if (!value) {
        return showError(fieldId, "Email address is required.");
      }
      // RFC-5322-ish simple regex
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        return showError(fieldId, "Please enter a valid email address.");
      }
      break;

    case "phone":
      if (!value) {
        return showError(fieldId, "Phone number is required.");
      }
      if (!/^\d{10}$/.test(value)) {
        return showError(fieldId, "Phone must be exactly 10 digits.");
      }
      break;

    case "event_id":
      if (!value) {
        return showError(fieldId, "Please select an event.");
      }
      break;

    case "tickets":
      if (!value || isNaN(value) || parseInt(value) < 1 || parseInt(value) > 10) {
        return showError(fieldId, "Tickets must be between 1 and 10.");
      }
      break;
  }

  return true;
}

/**
 * Display an inline error for a form field.
 * @param {string} fieldId
 * @param {string} message
 * @returns {false}
 */
function showError(fieldId, message) {
  const el    = document.getElementById(fieldId);
  const error = document.getElementById(fieldId + "Error");
  if (el)    el.classList.add("input-error");
  if (error) error.textContent = message;
  return false;
}

/**
 * Remove the error state from a field.
 * @param {string} fieldId
 */
function clearError(fieldId) {
  const el    = document.getElementById(fieldId);
  const error = document.getElementById(fieldId + "Error");
  if (el)    el.classList.remove("input-error");
  if (error) error.textContent = "";
}


/* ── Live Search (Events Page) ── */
/**
 * Filter event cards in real-time without reloading the page.
 * Reads the search input value and hides cards that do not match.
 */
function liveSearch() {
  const input = document.getElementById("searchInput");
  if (!input) return;

  const query = input.value.toLowerCase().trim();
  const cards = document.querySelectorAll("#eventsGrid .event-card");
  let visibleCount = 0;

  cards.forEach(card => {
    const name = (card.dataset.name || "").toLowerCase();
    const desc = (card.dataset.desc || "").toLowerCase();
    const match = !query || name.includes(query) || desc.includes(query);
    card.style.display = match ? "" : "none";
    if (match) visibleCount++;
  });

  // Update results count label
  const countEl = document.getElementById("resultsCount");
  if (countEl) {
    const label = visibleCount === 1 ? "event" : "events";
    countEl.innerHTML = `Showing <strong>${visibleCount}</strong> ${label}`;
  }
}
