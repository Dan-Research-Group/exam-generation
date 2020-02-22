{
    "questions": [
        {
            "prompt":"<b>what is $$1 + 1$$?</b>",
            "choices": [
                "<b>equals to 2</b>", "<b>equals to 0</b>", "<b>equals to 1</b>"
            ],
            "answers": 0
        },
        {
            "prompt":"<em>Who's the best Professor?</em>",
            "choices": [
                "Dan", "Denero", "Hug", "Hilfinger"
            ],
            "answers": [0, 1, 2, 3]
        },
        {
            "prompt":"Corporate needs you to the find differences between these 2 pictures.",
            "choices": [
                "image 1", "image 2"
            ],
            "answers": [1],
            "images": [
                {
                    "first image": "<encoded PNG image string>"
                },
                {
                    "type":"jpg",
                    "second image": "<encoded JPG image string>",
                }
            ]
        }
    ]
}

import random

class speedUp:

    def __init__(self, config):
        self.config = config

    def constructAQuestion(self, choice_number_index, choices, prompt_arg):
        return {
            "prompt" : self.config["prompt"].format(prompt_arg),
            "choices" : choices,
            "answers" : choice_number_index
        }

    def constructQuestions(self):
        num_questions = self.config["num_questions"]
        choices = self.config["choice_numbers"][:]
        if self.config["include_none_of_the_above"]:
            choices.append("None of the above")

        assert num_questions <= len(choices)

        questions = []
        
        picked_answers = random.sample(range(len(choices)), num_questions)
        for i in range(num_questions):
            cur_answer = picked_answers[i]
            c = [(choices[i], i == cur_answer) for i in range(len(choices))]
            if self.config["shuffle_choices"]:
                random.shuffle(c)
            cur_answer = [i for i in range(len(c)) if c[i][1]][0]
            c = [pair[0] for pair in c]
            
            if type(c[cur_answer]) is int:
                questions.append(self.constructAQuestion(cur_answer, c, int(100/c[cur_answer])))
            else:
                while True:
                    n = random.randrange(5, 96, 5)
                    if n not in c:
                        questions.append(self.constructAQuestion(cur_answer, c, int(100/n)))
                        break
        return {
            "questions" : questions
        }



# Class to parse JSON input file
# The updated config will be consumed by speedUp object
class updateConfig:


    def __init__(self, fp):
        self.fp = fp


# Class to turn speedUp object into JSON
# that will be output
class outputJSON:

    def __init__(self, speedUp, fp):
        self.speedUp = speedUp
        self.fp = fp