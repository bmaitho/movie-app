// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDmAjH4eO8C9ZKl1o8Tt73-5yi9ZYtIgs4",
  authDomain: "mtandao-dfdb3.firebaseapp.com",
  projectId: "mtandao-dfdb3",
  storageBucket: "mtandao-dfdb3.appspot.com",
  messagingSenderId: "771367078473",
  appId: "1:771367078473:web:368a7da2741765efb88d98",
  measurementId: "G-ZXD27WX65G"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
export { auth };