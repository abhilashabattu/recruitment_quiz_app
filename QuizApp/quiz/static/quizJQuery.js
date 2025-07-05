 $(document).ready(function() {
            // Quiz state variables
            let currentDomainIndex = 0;
            let currentQuestionIndex = 0;
            let timeLimit = 30 * 60; // 30 minutes for the whole quiz
            let timeLeft = timeLimit;
            let timerInterval;
            let userAnswers = {};
            
            // Initialize the quiz
            function initQuiz() {
                // Initialize answers storage
                $('.domain-section').each(function() {
                    const domain = $(this).attr('id').replace('section-', '');
                    userAnswers[domain] = new Array($(this).find('.question-panel').length).fill(null);
                });
                
                setupQuestionNav();
                updateProgress();
                startTimer();
                showQuestion(currentDomainIndex, currentQuestionIndex);
                
                // Event handlers
                $('#prev-btn').click(prevQuestion);
                $('#next-btn').click(nextQuestion);
                $('#prev-section-btn').click(prevSection);
                $('#next-section-btn').click(nextSection);
                
                // Track radio button selections
                $('input[type="radio"]').change(function() {
                    const questionId = $(this).closest('.question-panel').attr('id').split('-').slice(1).join('-');
                    const domain = $(this).closest('.domain-section').attr('id').replace('section-', '');
                    userAnswers[domain][currentQuestionIndex] = $(this).val();
                    updateQuestionNav(currentQuestionIndex, true);
                });
                
                // Form submission handler
                $('#quizForm').submit(function(e) {
                    const unanswered = getUnansweredCount();
                    if (unanswered > 0) {
                        if (!confirm(`You have ${unanswered} unanswered questions. Are you sure you want to submit?`)) {
                            e.preventDefault();
                        }
                    }
                });
            }

            // Set up question navigation sidebar
            function setupQuestionNav() {
                const $nav = $('#question-nav');
                $nav.empty();
                
                let questionNumber = 1;
                $('.domain-section').each(function() {
                    const domain = $(this).attr('id').replace('section-', '');
                    
                    // Add domain heading
                    $nav.append(`
                        <div class="list-group-item domain-header bg-dark text-white fw-bold">
                            <i class="fas 
                                {% if domain == 'java' %} fa-java
                                {% elif domain == 'python' %} fa-python
                                {% elif domain == 'css' %} fa-css3-alt
                                {% elif domain == 'html' %} fa-html5
                                {% elif domain == 'javascript' %} fa-js
                                {% elif domain == 'jquery' %} fa-code
                                {% else %} fa-laptop-code
                                {% endif %} 
                                me-2"></i>
                            ${domain.charAt(0).toUpperCase() + domain.slice(1)}
                        </div>
                    `);
                    
                    // Add questions for this domain
                    $(this).find('.question-panel').each(function(index) {
                        $nav.append(`
                            <a href="#" class="list-group-item list-group-item-action question-nav-item ps-4" 
                               data-domain="${domain}" 
                               data-qid="${index}">
                                <i class="fas fa-question-circle me-2"></i>Question ${questionNumber}
                                <span class="badge bg-secondary float-end">${questionNumber}</span>
                            </a>
                        `);
                        questionNumber++;
                    });
                });
                
                $('.question-nav-item').click(function(e) {
                    e.preventDefault();
                    const domain = $(this).data('domain');
                    const qid = $(this).data('qid');
                    const domainIndex = $('.domain-section').index($(`#section-${domain}`));
                    currentQuestionIndex = qid;
                    showQuestion(domainIndex, currentQuestionIndex);
                });
            }

            // Update question navigation appearance
            function updateQuestionNav(qid, answered) {
                const $navItem = $('.question-nav-item').eq(qid);
                const $badge = $navItem.find('.badge');
                
                if (answered) {
                    $badge.removeClass('bg-secondary').addClass('bg-success');
                } else {
                    $badge.removeClass('bg-success').addClass('bg-secondary');
                }
            }

            // Show specific question in current section
            function showQuestion(domainIndex, questionIndex) {
                const domain = $('.domain-section').eq(domainIndex).attr('id').replace('section-', '');
                
                // Hide all questions in all sections
                $('.question-panel').hide();
                
                // Show the selected question
                $(`#question-${domain}-${questionIndex}`).show();
                
                // Update current indices
                currentDomainIndex = domainIndex;
                currentQuestionIndex = questionIndex;
                
                // Update UI elements
                updateNavButtons();
                updateProgress();
                
                // Update counters
                const totalQuestions = $('.question-panel').length;
                $('#question-counter').text(`Question ${getGlobalQuestionIndex() + 1} of ${totalQuestions}`);
                
                // Update section title
                $('#current-domain-title').text(`${domain.charAt(0).toUpperCase() + domain.slice(1)} Quiz`);
                
                // Update active nav item
                $('.question-nav-item').removeClass('active');
                const globalIndex = getGlobalQuestionIndex();
                const $navItems = $('.question-nav-item');
                if ($navItems.length > globalIndex) {
                    $navItems.eq(globalIndex).addClass('active');
                    
                    // Scroll to the active question
                    const $activeNav = $navItems.eq(globalIndex);
                    const $navContainer = $('#question-nav');
                    const navScrollTop = $navContainer.scrollTop();
                    const navHeight = $navContainer.height();
                    const itemOffset = $activeNav.offset().top - $navContainer.offset().top + navScrollTop;
                    
                    if (itemOffset < navScrollTop || itemOffset > navScrollTop + navHeight - $activeNav.outerHeight()) {
                        $navContainer.animate({
                            scrollTop: itemOffset - navHeight/2
                        }, 200);
                    }
                }
                
                // Restore selected answer if exists
                if (userAnswers[domain][questionIndex] !== null) {
                    $(`#question-${domain}-${questionIndex} input[value="${userAnswers[domain][questionIndex]}"]`).prop('checked', true);
                }
            }

            // Get global question index across all sections
            function getGlobalQuestionIndex() {
                let globalIndex = 0;
                let found = false;
                
                $('.domain-section').each(function(domainIdx) {
                    if (domainIdx < currentDomainIndex) {
                        globalIndex += $(this).find('.question-panel').length;
                    } else if (domainIdx === currentDomainIndex) {
                        globalIndex += currentQuestionIndex;
                        found = true;
                        return false; // break the loop
                    }
                });
                
                return found ? globalIndex : 0;
            }
            
            // Get count of unanswered questions
            function getUnansweredCount() {
                let unanswered = 0;
                for (const domain in userAnswers) {
                    unanswered += userAnswers[domain].filter(answer => answer === null).length;
                }
                return unanswered;
            }
            
            // Update navigation buttons state
            function updateNavButtons() {
                const domain = $('.domain-section').eq(currentDomainIndex).attr('id').replace('section-', '');
                const totalQuestionsInSection = $(`#section-${domain} .question-panel`).length;
                const totalDomains = $('.domain-section').length;
                
                // Question navigation buttons
                $('#prev-btn').prop('disabled', currentQuestionIndex === 0);
                
                if (currentQuestionIndex === totalQuestionsInSection - 1) {
                    $('#next-btn').addClass('d-none');
                    if (currentDomainIndex < totalDomains - 1) {
                        $('#next-section-btn').removeClass('d-none');
                    } else {
                        $('#submit-btn').removeClass('d-none');
                    }
                } else {
                    $('#next-btn').removeClass('d-none');
                    $('#next-section-btn').addClass('d-none');
                    $('#submit-btn').addClass('d-none');
                }
                
                // Section navigation buttons
                $('#prev-section-btn').prop('disabled', currentDomainIndex === 0);
            }

            // Update progress bar
            function updateProgress() {
                const totalQuestions = $('.question-panel').length;
                const answered = totalQuestions - getUnansweredCount();
                const progress = (answered / totalQuestions) * 100;
                $('#quiz-progress').css('width', `${progress}%`).attr('aria-valuenow', progress);
            }
            
            // Navigation functions
            function prevQuestion() {
                if (currentQuestionIndex > 0) {
                    showQuestion(currentDomainIndex, currentQuestionIndex - 1);
                }
            }
            
            function nextQuestion() {
                const domain = $('.domain-section').eq(currentDomainIndex).attr('id').replace('section-', '');
                const totalQuestionsInSection = $(`#section-${domain} .question-panel`).length;
                
                if (currentQuestionIndex < totalQuestionsInSection - 1) {
                    showQuestion(currentDomainIndex, currentQuestionIndex + 1);
                }
            }
            
            function prevSection() {
                if (currentDomainIndex > 0) {
                    currentQuestionIndex = 0;
                    showQuestion(currentDomainIndex - 1, currentQuestionIndex);
                }
            }
            
            function nextSection() {
                if (currentDomainIndex < $('.domain-section').length - 1) {
                    currentQuestionIndex = 0;
                    showQuestion(currentDomainIndex + 1, currentQuestionIndex);
                }
            }
            
            // Timer functions
            function startTimer() {
                updateTimerDisplay();
                timerInterval = setInterval(function() {
                    timeLeft--;
                    updateTimerDisplay();
                    
                    if (timeLeft <= 0) {
                        clearInterval(timerInterval);
                        $('#quizForm').submit();
                    }
                }, 1000);
            }
            
            function updateTimerDisplay() {
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                $('#timer').text(`${minutes}:${seconds < 10 ? '0' : ''}${seconds}`);
                
                // Visual warnings
                if (timeLeft <= 300) { // 5 minutes
                    $('#timer').parent().removeClass('bg-danger').addClass('bg-warning');
                }
                if (timeLeft <= 60) { // 1 minute
                    $('#timer').parent().removeClass('bg-warning').addClass('bg-danger');
                }
            }
            
            // Initialize the quiz
            initQuiz();
        });