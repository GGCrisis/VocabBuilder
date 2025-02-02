const speedGamePage = document.getElementById("speed-game-page");
        const flashcardsGamePage = document.getElementById("flashcards-game-page");
        const timerElement = document.getElementById("timer");
        let timer;
        let timeLeft;

        // Show Speed Game
        document.getElementById("showSpeedGame").addEventListener("click", () => {
            document.getElementById("home-page").style.display = "none";
            speedGamePage.style.display = "block";
            startTimer(120);
        });

        // Show Pronunciation Game
        document.getElementById("showPronunciationGame").addEventListener("click", () => {
            document.getElementById("home-page").style.display = "none";
            document.getElementById("pronunciation-game-page").style.display = "block";
        });

        // Show Flashcards Game
        document.getElementById("showFlashcardsGame").addEventListener("click", () => {
            document.getElementById("home-page").style.display = "none";
            flashcardsGamePage.style.display = "block";
            startTimer(120); // Start the timer for Flashcards game
            loadNextWord();  // Load flashcard data
        });

        // Scenarios Game
        document.getElementById("scenariosGame").addEventListener("click", () => {
            const userPlace = prompt("Enter a place you're going to:");
            if (userPlace) {
                fetch('/scenario', {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ place: userPlace }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.words) {
                            // Display the scenario name
                            document.getElementById("scenario-name").innerText = userPlace;

                            // Clear previous results
                            const wordList = document.getElementById("word-list");
                            wordList.innerHTML = "";

                            // Add each word and meaning to the list
                            data.words.forEach(item => {
                                const li = document.createElement("li");
                                li.innerHTML = `<strong>${item.word}</strong>: ${item.meaning}`;
                                wordList.appendChild(li);
                            });

                            // Show the results section
                            document.getElementById("scenario-results").style.display = "block";
                        } else {
                            alert(data.error || "Failed to fetch words for the scenario.");
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        alert("An error occurred while fetching scenario words.");
                    });
            }
        });

        // Timer functionality
        function startTimer(duration) {
            timeLeft = duration;
            updateTimer(); // Update timer display
            timer = setInterval(() => {
                timeLeft--;
                updateTimer();
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    alert("Time's up!");
                    goHome(); // Return to the home page when the timer ends
                }
            }, 1000);
        }

        function updateTimer() {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerElement.innerText = `Time Remaining: ${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;
        }

        function goHome() {
            document.getElementById("home-page").style.display = "block";
            speedGamePage.style.display = "none";
            flashcardsGamePage.style.display = "none";
            document.getElementById("pronunciation-game-page").style.display = "none";
            clearInterval(timer); // Clear timer when going home
        }
        // Fetch flashcard data from Flask API
        function loadNextWord() {
            console.log("Fetching next word..."); // Debug log
            fetch('http://127.0.0.1:5000/next_word')
                .then(response => {
                    console.log("Response received:", response); // Debug log
                    return response.json();
                })
                .then(data => {
                    console.log("Data received:", data); // Debug log
                    if (data.word) {
                        document.getElementById("word").innerText = `Word: ${data.word}`;
                        document.getElementById("meaning").innerText = `Meaning: ${data.meaning}`;
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error loading word:', error);
                });
        }
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import {getAuth, onAuthStateChanged, signOut} from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import{getFirestore, getDoc, doc} from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js"

const firebaseConfig = {
    // Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyC8e1dTP0BfiFJNmpHW2qaabxhilV-c9pk",
  authDomain: "vocab-f7a82.firebaseapp.com",
  projectId: "vocab-f7a82",
  storageBucket: "vocab-f7a82.firebasestorage.app",
  messagingSenderId: "774294339159",
  appId: "1:774294339159:web:fbe24bba54d72e82dfed12"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
  };
 
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);

  const auth=getAuth();
  const db=getFirestore();

  onAuthStateChanged(auth, (user)=>{
    const loggedInUserId=localStorage.getItem('loggedInUserId');
    if(loggedInUserId){
        console.log(user);
        const docRef = doc(db, "users", loggedInUserId);
        getDoc(docRef)
        .then((docSnap)=>{
            if(docSnap.exists()){
                const userData=docSnap.data();
                document.getElementById('loggedUserFName').innerText=userData.firstName;
                document.getElementById('loggedUserEmail').innerText=userData.email;
                document.getElementById('loggedUserLName').innerText=userData.lastName;

            }
            else{
                console.log("no document found matching id")
            }
        })
        .catch((error)=>{
            console.log("Error getting document");
        })
    }
    else{
        console.log("User Id not Found in Local storage")
    }
  })

  const logoutButton=document.getElementById('logout');

  logoutButton.addEventListener('click',()=>{
    localStorage.removeItem('loggedInUserId');
    signOut(auth)
    .then(()=>{
        window.location.href='index.html';
    })
    .catch((error)=>{
        console.error('Error Signing out:', error);
    })
  })
  // Function to show a dropdown section
function showDropdown(sectionId) {
    // Hide all dropdown sections
    document.querySelectorAll('.dropdown-section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected section
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    }
}

// Function to hide a dropdown section
function hideDropdown(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'none';
    }
}

// Add event listeners to Leaderboard and Coins links
document.querySelector('.leaderboard-link').addEventListener('click', () => {
    showDropdown('leaderboard');
});

document.querySelector('.coins-link').addEventListener('click', () => {
    showDropdown('coins');
});

