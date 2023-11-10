import { initializeApp } from "firebase/app"
import { getFirestore } from "firebase/firestore"

const firebaseConfig = {
  apiKey: "AIzaSyBHiMCajNeVJhGgBFyGw-DdVoWDHzydOjw",
  authDomain: "demorepo-243a7.firebaseapp.com",
  projectId: "demorepo-243a7",
  storageBucket: "demorepo-243a7.appspot.com",
  messagingSenderId: "329008802572",
  appId: "1:329008802572:web:ed3050f30ea7c16281f729",
  measurementId: "G-9FPCMETH0B",
}

export const app = initializeApp(firebaseConfig)
export const db = getFirestore(app)
