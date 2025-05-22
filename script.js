document.addEventListener("DOMContentLoaded", function () {
    const questions = [
        "Database Fundamentals", "Computer Architecture", "Distributed Computing Systems",
        "Cyber Security", "Networking", "Software Development", "Programming Skills",
        "Project Management", "Computer Forensics Fundamentals", "Technical Communication",
        "AI ML", "Software Engineering", "Business Analysis", "Communication skills",
        "Data Science", "Troubleshooting skills", "Graphics Designing"
    ];

    const options = ["Not Interested", "Beginner", "Poor", "Average", "Intermediate", "Excellent", "Professional"];
    const questionsContainer = document.getElementById("questionsContainer");

    // Dynamically generate the questions
    questions.forEach((question, index) => {
        let questionDiv = document.createElement("div");
        questionDiv.classList.add("question-block");

        let label = document.createElement("label");
        label.innerText = `${index + 1}. ${question}`;
        questionDiv.appendChild(label);

        let select = document.createElement("select");
        select.name = `question${index}`;
        select.required = true;

        let defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.innerText = "Select an answer";
        select.appendChild(defaultOption);

        options.forEach(option => {
            let opt = document.createElement("option");
            opt.value = option;
            opt.innerText = option;
            select.appendChild(opt);
        });

        questionDiv.appendChild(select);
        questionsContainer.appendChild(questionDiv);
    });

    // Handle form submission
    document.getElementById("quizForm").addEventListener("submit", function (event) {
        event.preventDefault();

        let userAnswers = {};
        let allAnswered = true;

        // Collect answers from the form
        questions.forEach((_, index) => {
            let selectedOption = document.querySelector(`select[name="question${index}"]`).value;
            if (selectedOption === "") {
                allAnswered = false;
            } else {
                // Convert answer to numerical value
                userAnswers[index] = options.indexOf(selectedOption); // Mapping to 0-6 scale
            }
        });

        // If not all questions are answered, show an alert
        if (!allAnswered) {
            alert("Please answer all questions before submitting.");
            return;
        }

        console.log("Submitting user answers:", userAnswers); // Debugging output

        // Send the collected answers to the backend for prediction
        fetch("http://127.0.0.1:5000/submit_quiz", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userAnswers) // Send answers as JSON
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Career Role Response:", data); // Debugging output
            alert(`Your recommended career role is: ${data.role}`);
            localStorage.setItem("careerRole", data.role);
            location.href = "finalresult.html"; // Redirect to result page
        })
        .catch(error => {
            console.error("Error fetching API:", error);
            alert("Something went wrong. Please try again.");
        });
    });
});
