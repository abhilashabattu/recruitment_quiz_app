$(document).ready(function() {

    let currentQuestion = 0;
    const totalQuestions = $('.question-panel').length;
    const timeLimit = 5 * 60; 
    let timeLeft = timeLimit;
    let timerInterval;
    let userAnswers = new Array(totalQuestions).fill(null);

    // Initialize the quiz
    function initQuiz() {
        
        setupQuestionNav();
        
        
        updateProgress();
        
        startTimer();
        
      
        showQuestion(currentQuestion);
        
        
        $('#prev-btn').click(prevQuestion);
        $('#next-btn').click(nextQuestion);
        $('#submit-btn').click(submitQuiz);
        
      
        $('input[type="radio"]').change(function() {
            const questionId = $(this).attr('name').split('-')[1];
            userAnswers[currentQuestion] = $(this).val();
            updateQuestionNav(currentQuestion, true);
        });
    }

   
    function setupQuestionNav() {
        const nav = $('#question-nav');
        nav.empty();
        
        for (let i = 0; i < totalQuestions; i++) {
            nav.append(`
                <a href="#" class="list-group-item list-group-item-action question-nav-item" data-qid="${i}">
                    Question ${i + 1}
                    <span class="badge bg-secondary float-end">${i + 1}</span>
                </a>
            `);
        }
        
        $('.question-nav-item').click(function(e) {
            e.preventDefault();
            const qid = $(this).data('qid');
            showQuestion(qid);
        });
    }

    // Show specific question
    function showQuestion(qid) {
        
        $('.question-panel').hide();
        
        
        $(`#question-${qid}`).show();
        
        
        currentQuestion = qid;
        
        
        updateNavButtons();
        
       
        $('#question-counter').text(`Question ${qid + 1} of ${totalQuestions}`);
        
       
        $('.question-nav-item').removeClass('active');
        $(`.question-nav-item[data-qid="${qid}"]`).addClass('active');
        
       
        if (userAnswers[qid] !== null) {
            $(`input[name="question-${qid}"][value="${userAnswers[qid]}"]`).prop('checked', true);
        }
    }

    
    function updateQuestionNav(qid, answered) {
        const $navItem = $(`.question-nav-item[data-qid="${qid}"]`);
        const $badge = $navItem.find('.badge');
        
        if (answered) {
            $badge.removeClass('bg-secondary').addClass('bg-success');
        } else {
            $badge.removeClass('bg-success').addClass('bg-secondary');
        }
    }

    // Update navigation 
    function updateNavButtons() {
        $('#prev-btn').prop('disabled', currentQuestion === 0);
        
        if (currentQuestion === totalQuestions - 1) {
            $('#next-btn').addClass('d-none');
            $('#submit-btn').removeClass('d-none');
        } else {
            $('#next-btn').removeClass('d-none');
            $('#submit-btn').addClass('d-none');
        }
    }

    // previous question
    function prevQuestion() {
        if (currentQuestion > 0) {
            showQuestion(currentQuestion - 1);
        }
    }

    // /Next question
    function nextQuestion() {
        if (currentQuestion < totalQuestions - 1) {
            showQuestion(currentQuestion + 1);
        }
    }

    // Update progress 
    function updateProgress() {
        const progress = ((currentQuestion + 1) / totalQuestions) * 100;
        $('#quiz-progress').css('width', `${progress}%`).attr('aria-valuenow', progress);
    }

    // Timer 
    function startTimer() {
        updateTimerDisplay();
        timerInterval = setInterval(function() {
            timeLeft--;
            updateTimerDisplay();
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                submitQuiz();
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        $('#timer').text(`${minutes}:${seconds < 10 ? '0' : ''}${seconds}`);
        
       
        if (timeLeft <= 60) {
            $('#timer').parent().removeClass('bg-danger').addClass('bg-warning');
        }
        if (timeLeft <= 30) {
            $('#timer').parent().removeClass('bg-warning').addClass('bg-danger');
        }
    }

    // Submit 
    function submitQuiz() {
        clearInterval(timerInterval);
        
        
        const quizData = {
            answers: userAnswers,
            timeTaken: timeLimit - timeLeft
        };
        
        // Send data to server 
        $.ajax({
            url: '/submit-quiz/',
            type: 'POST',
            data: JSON.stringify(quizData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
              
                window.location.href = '/quiz-results/';
            },
            error: function(xhr) {
                alert('Error submitting quiz. Please try again.');
            }
        });
    }

    //  CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initialize the quiz
    initQuiz();
});