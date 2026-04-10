
// import axios from "axios";

class Interactions{
    constructor(){
         this.interact_container = document.querySelector(".interact")
    }

    question_pipeline(){
        let user_prompt = document.querySelector("textarea").value
        this.add_question("user", user_prompt)
        document.querySelector("textarea").value = ""

        fetch('http://127.0.0.1:8000/agent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: user_prompt })
        })
        .then(res => {
            if (!res.ok) {
                throw new Error("Erreur HTTP " + res.status)
            }
            return res.json()
        })
        .then(data => {
            console.log("appel réussi")
            this.add_question("agent", data.response)
        })
        .catch(err => {
            console.log("une erreur s'est produite !!!:", err)
            this.add_question("agent", "Une erreur s'est produite.")
        })

            
        
        
        
        
        
        
        }
    get_response(){
        ErrorEvent
    }
    add_question(type, data){
        let question = document.createElement("div")
        question.className = "question"
        question.innerHTML = `
                                <div class="${type}">
                                    <p class="data"><pre>${data}</pre></p>
                                </div>
                            `
        this.interact_container.appendChild(question)
        
    }
    

}


const interact_ = new Interactions()