$(document).ready(function() {
    // Cache DOM elements
    const $cards = $('.selectable-card');
    const $checkboxes = $('.domain-checkbox');
    const $startBtn = $('#startQuizBtn');
    const $selectedCount = $('#selectedCount');
    const $quizForm = $('#quizSelectionForm');

    // Card selection functionality
    $cards.on('click', function(e) {
        // Don't toggle if clicking on the checkbox itself
        if (!$(e.target).is('input[type="checkbox"]')) {
            const $checkbox = $(this).find('.domain-checkbox');
            $checkbox.prop('checked', !$checkbox.prop('checked'));
            updateSelection();
        }
    });

    // Checkbox click handler
    $checkboxes.on('click', function(e) {
        e.stopPropagation();
        updateSelection();
    });

    // Update selection UI
    function updateSelection() {
        const selectedCount = $checkboxes.filter(':checked').length;
        $selectedCount.text(selectedCount);
        $startBtn.toggleClass('d-none', selectedCount === 0);
        
        $cards.each(function() {
            $(this).toggleClass('selected', $(this).find('.domain-checkbox').is(':checked'));
        });
    }

    // Initialize
    updateSelection();
    
    
});