# ---------- COLORS ----------
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# ---------- STATE ----------
sumofyourrun = 0
sumofcomp = 0
wickets = 0
compwickets = 0
balls = 0
target = None
bat_runs_per_over = []
bowl_runs_per_over = []
current_graph = None

striker = ""
non_striker = ""

# ---------- TRACKING ----------
bat_stats = {}
bowl_stats = {}
fall_of_wickets = []
partnerships = []

runs_per_over = []
current_over_runs = 0

pair_runs = 0
pair_balls = 0
current_pair = []

user_history = []

print("LOADING! PLEASE WAIT FOR A BIT ...")

import random
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from gtts import gTTS
import os



def momentum_check():
    if len(win_prob_history) < 2:
        return

    change = win_prob_history[-1] - win_prob_history[-2]

    pos_lines = [
        "Momentum is shifting towards the batting side!",
        "The pressure is turning on the bowlers!",
        "Batting side gaining strong control now!"
    ]

    neg_lines = [
        "Massive setback for the batting side!",
        "Bowling team taking control of the game!",
        "That changes everything in this match!"
    ]

    if change >= 10:
        line = random.choice(pos_lines)
        print(GREEN + "🔥 " + line + RESET)
        speak(line)

    elif change <= -10:
        line = random.choice(neg_lines)
        print(RED + "💥 " + line + RESET)
        speak(line)

        
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("voice.mp3")

       
        os.system("start voice.mp3")

    except:
        pass

win_prob_history = []

def calculate_win_prob():
    global prob
    if not target:
        return 50  # first innings

    balls_left = total_balls - balls
    runs_needed = target - sumofcomp
    wkts_left = noofwickets - compwickets

    if runs_needed <= 0:
        return 100
    if balls_left <= 0:
        return 0

    rrr = runs_needed / balls_left

    # 🔥 Core logic
    prob = 50

    prob -= rrr * 15          
    prob += wkts_left * 3     

    prob = max(0, min(100, prob))
    return prob



def show_win_prob_graph() :

    if not win_prob_history:
        return

    x = list(range(1, len(win_prob_history) + 1))

    plt.figure()
    plt.plot(x, win_prob_history, marker='o')
    plt.xlabel("Balls")
    plt.ylabel("Win Probability (%)")
    plt.title("Win Probability (Live)")
    plt.ylim(0, 100)
    plt.show()

def show_live_graph():
    if len(current_graph) == 0:
        print("No graph data yet")
        return

    plt.figure()
    plt.plot(range(1, len(current_graph)+1), current_graph, marker='o')
    plt.xlabel("Overs")
    plt.ylabel("Runs")
    plt.title("Runs per Over (Live)")

    plt.grid(True)
    plt.show(block=True)

l = [1,2,3,4,5,6]
f = [7,8]

print("Initialising... \nDONE!")
# ---------- INPUT ----------
team = input("Enter team name: ").title() or "You"
overs = int(input("Overs: "))
total_balls = overs * 6

difficulty = input(RED + "AI Difficulty (easy/hard/insane): ").lower()
if difficulty not in ["easy","hard","insane"]:
    difficulty = "hard"

try:
    noofwickets = int(input("Wickets: "))
except:
    noofwickets = 10


# ---------- INIT ----------
def new_batsman(name):
    if name not in bat_stats:
        bat_stats[name] = {"runs":0,"balls":0,"4s":0,"6s":0}

def new_bowler(name):
    if name not in bowl_stats:
        bowl_stats[name] = {"runs":0,"balls":0,"wkts":0}

# ---------- SMART AI ----------
def smart_ai(user_input, chasing=False):
    user_history.append(user_input)
    if len(user_history) > 10:
        user_history.pop(0)

    predicted = max(set(user_history), key=user_history.count)

    if difficulty == "easy":
        return random.choice(l)

    if difficulty == "hard" and random.random() < 0.3:
        return predicted

    if difficulty == "insane":
        if random.random() < 0.5:
            return predicted

        if chasing and target:
            balls_left = total_balls - balls
            need = target - sumofcomp
            if balls_left > 0:
                rrr = need / balls_left
                if rrr > 1.5:
                    return random.choice([4,5,6])
                elif rrr < 0.8:
                    return random.choice([1,2,3])

    return random.choice(l)

# ---------- DISPLAY ----------
def scoreboard(score, wkts):
    crr = (score/(balls/6)) if balls else 0
    print(YELLOW + f"{score}/{wkts} in {balls//6}.{balls%6} overs | CRR: {crr:.2f}" + RESET)

def target_display(current):
    if target:
        balls_left = total_balls - balls
        need = target - current
        if need > 0 and balls_left > 0:
            rrr = (need/(balls_left/6))
            print(YELLOW + f"Need {need} in {balls_left} balls | RRR: {rrr:.2f}" + RESET)

def show_live():
    print(YELLOW + "\n--- LIVE ---" + RESET)
    if striker in bat_stats:
        s = bat_stats[striker]
        print(GREEN + f"{striker}: {s['runs']}({s['balls']})")
    if non_striker in bat_stats:
        ns = bat_stats[non_striker]
        print(BLUE + f"{non_striker}: {ns['runs']}({ns['balls']})")
    
    
    

# ---------- GRAPH ----------
def show_graph():
    print("\n📊 Runs per Over\n")

    if not runs_per_over:
        print("No data to display")
        return

    for i, runs in enumerate(runs_per_over, 1):
        bars = "█" * (runs // 2) if runs > 0 else ""
        print(f"Over {i:02}: {bars} ({runs})")

# ---------- COMMENTARY ----------
def commentary(run, wicket=False):

    wicket_lines = [
        "He's gone! What a wicket!",
        "That is a huge breakthrough!",
        "Clean bowled! Absolute beauty!",
        "Big wicket at the right time!",
        "And that's out! The crowd erupts!"
    ]

    six_lines = [
        "That's massive! Six runs!",
        "Into the stands! What a hit!",
        "He has absolutely smashed that!",
        "That ball is out of the ground!",
        "Huge six! Pure power!"
    ]

    four_lines = [
        "Beautiful shot! That's four!",
        "Driven to perfection for four!",
        "Cracking shot through the gap!",
        "That's racing away to the boundary!",
        "Four runs! Classy stroke!"
    ]

    run_lines = [
        "Quick single taken",
        "Good running between the wickets",
        "They come back for more runs",
        "Nice placement for a couple",
        "Smart cricket there"
    ]

    # 🎙 Simulated commentator tag (optional feel)
    commentator = random.choice([
        "🎙 Commentator:",
        "📢 Analyst:",
        "🎤 Broadcaster:"
    ])

    if wicket:
        line = random.choice(wicket_lines)
        print(RED + f"{commentator} {line}" + RESET)
        speak(line)

    else:
        if run == 6:
            line = random.choice(six_lines)
            print(GREEN + f"{commentator} {line}" + RESET)
            speak(line)

        elif run == 4:
            line = random.choice(four_lines)
            print(GREEN + f"{commentator} {line}" + RESET)
            speak(line)

        elif run in [1,2,3]:
            line = random.choice(run_lines)
            print(BLUE + f"{commentator} {line}" + RESET)
            speak(line)

# ---------- BATTING ----------
def bat():
    global sumofyourrun, wickets, balls, striker, non_striker
    global pair_runs, pair_balls, current_pair, current_over_runs

    if wickets == 0 and balls == 0:
        striker = input(YELLOW + "Striker: ").title()
        non_striker = input(BLUE + "Non-Striker: ").title()
        current_pair = [striker, non_striker]
        new_batsman(striker)
        new_batsman(non_striker)
    else:
        striker = input(YELLOW +"New Batsman: ").title()
        current_pair[0] = striker
        new_batsman(striker)

    while True:
        if balls >= total_balls:
            if current_over_runs > 0:
                current_graph.append(current_over_runs)
            return "end"

        try:
            run = int(input(GREEN + f"{striker} → Run: "))
        except:
            continue

        if run not in l:
            continue

        comp = smart_ai(run)
        print(f"Computer: {comp}")

        balls += 1
        bat_stats[striker]["balls"] += 1

       
        if run == comp:
            commentary(0, True)

            fall_of_wickets.append(f"{sumofyourrun}/{wickets+1} ({striker})")
            partnerships.append(f"{current_pair[0]} & {current_pair[1]} : {pair_runs} ({pair_balls})")

            pair_runs = 0
            pair_balls = 0

            wickets += 1

            calculate_win_prob()
            momentum_check()

            scoreboard(sumofyourrun, wickets)

            if balls % 6 == 0:
                striker, non_striker = non_striker, striker
                current_graph.append(current_over_runs)
                
                current_over_runs = 0

                print(YELLOW + "Over End" + RESET)

                calculate_win_prob()
                win_prob_history.append(calculate_win_prob())

                scoreboard(sumofyourrun, wickets)   
                show_live()                         

                show_live_graph()
                show_win_prob_graph()

                print("\nPartnerships:")
                for p in partnerships:
                    print(p)

                scoreboard(sumofyourrun, wickets)
                show_live()
                target_display(sumofyourrun)

            return

        
        sumofyourrun += run
        current_over_runs += run
        bat_stats[striker]["runs"] += run

        pair_runs += run
        pair_balls += 1

        commentary(run)

        calculate_win_prob()
        momentum_check()

        if target and sumofyourrun >= target:
            print(GREEN + f"{team} WON!" + RESET)
            current_graph.append(current_over_runs)
            return "end"

        if run % 2 == 1:
            striker, non_striker = non_striker, striker

        if balls % 6 == 0:
            striker, non_striker = non_striker, striker
            current_graph.append(current_over_runs)
            current_over_runs = 0

            calculate_win_prob()
            win_prob_history.append(calculate_win_prob())

            print(YELLOW + "Over End" + RESET)

            scoreboard(sumofyourrun, wickets)   # ✅ ADD THIS
            show_live()                         # ✅ ADD THIS

            show_live_graph()
            show_win_prob_graph()

            print("\nPartnerships:")
            for p in partnerships:
                print(p)

        scoreboard(sumofyourrun, wickets)
        show_live()
        target_display(sumofyourrun)

# ---------- BOWLING ----------
def bowl():
    global sumofcomp, compwickets, balls, current_over_runs

    bowler = input(GREEN +"Bowler (this over): ").title()
    new_bowler(bowler)

    balls_in_over = 0

    while True:
        if balls >= total_balls:
            if current_over_runs > 0:
                current_graph.append(current_over_runs)
            return "end"

        if balls_in_over == 6:
            current_graph.append(current_over_runs)
            current_over_runs = 0

            print(YELLOW + f"Over completed by {bowler}" + RESET)

            scoreboard(sumofcomp, compwickets)
            

            show_live_graph()
            show_win_prob_graph()

            print("\nPartnerships:")
            for p in partnerships:
                    print(p)

            return

        try:
            run = int(input("Your number: "))
        except:
            continue

        if run not in l:
            continue

        comp = smart_ai(run, True)
        print(f"Computer: {comp}")

        balls += 1
        balls_in_over += 1
        bowl_stats[bowler]["balls"] += 1

        # ======================
        # 🚨 WICKET FIRST
        # ======================
        if comp == run:
            commentary(0, True)

            compwickets += 1
            bowl_stats[bowler]["wkts"] += 1

            calculate_win_prob()
            win_prob_history.append(calculate_win_prob())

            momentum_check()

            scoreboard(sumofcomp, compwickets)
            show_live_graph()
            show_win_prob_graph()


            if compwickets >= noofwickets:
                current_graph.append(current_over_runs)
                return "end"

            continue

        # ======================
        # ✅ NORMAL BALL
        # ======================
        sumofcomp += comp
        current_over_runs += comp
        bowl_stats[bowler]["runs"] += comp

        commentary(comp)

        calculate_win_prob()
        win_prob_history.append(calculate_win_prob())

        momentum_check()

        print(YELLOW + f"Win Probability: {calculate_win_prob():.1f}%" + RESET)

        scoreboard(sumofcomp, compwickets)
        
        target_display(sumofcomp)

        if target and sumofcomp >= target:
            print(RED + "Computer WON!" + RESET)
            current_graph.append(current_over_runs)
            return "end"

# ---------- INNINGS ----------
def first_innings():
    global current_graph
    current_graph = bat_runs_per_over
    global balls, current_over_runs
    balls = 0
    current_over_runs = 0
    while wickets < noofwickets and balls < total_balls:
        if bat() == "end":
            break
        


def second_innings():
    global current_graph
    current_graph = bowl_runs_per_over
    global balls, current_over_runs
    balls = 0
    current_over_runs = 0
    while compwickets < noofwickets and balls < total_balls:
        if bowl() == "end":
            break

# ---------- TOSS ----------
toss = input(RED + "Heads or Tails: ")
toss1 = "Heads" if "h" in toss.lower() else "Tails"

choice = {"Heads":7,"Tails":8}[toss1]
tosswon = random.choice(f)
well = {7:"Heads",8:"Tails"}[tosswon]

print(GREEN + f"You chose {toss1}", end = "") 
print(YELLOW + f", Coin: {well}")


# ---------- GAME ----------
if tosswon == choice:
    decision = input(GREEN + "Bat or Bowl: ").lower()
    if "bat" in decision:
        first_innings()
        target = sumofyourrun + 1
        print(RED + f"Target : {target}")
        second_innings()
    else:
        second_innings()
        target = sumofcomp + 1
        print(RED + f"Target : {target}")
        first_innings()
else:
    comp_decision = random.choice(["bat","bowl"])
    print(RED + f"Computer chose to {comp_decision.upper()}")

    if comp_decision == "bat":
        second_innings()

        target = sumofcomp + 1
        print(RED + f"Target : {target}")
        first_innings()
    else:
        first_innings()
        target = sumofyourrun + 1
        print(RED + f"Target : {target}")
        second_innings()

# ---------- RESULT ----------
print("\n" + "="*50)
print("RESULT")
print("="*50)

if sumofyourrun > sumofcomp:
    print(GREEN + f"{team} WON THE MATCH!" + RESET)
elif sumofcomp > sumofyourrun:
    print(RED + "COMPUTER WON THE MATCH!" + RESET)
else:
    print(YELLOW + "MATCH DRAW" + RESET)

# ---------- FULL SCORECARD ----------
print("\nFULL SCORECARD\n")

# ---- BATTING ----
for p, d in bat_stats.items():
    runs = d["runs"]
    balls_faced = d["balls"]
    sr = (runs / balls_faced * 100) if balls_faced else 0
    print(f"{p}: {runs}({balls_faced}) SR:{sr:.2f}")

# ---- BOWLING ----
print("\nBOWLING")
for b, d in bowl_stats.items():
    balls_bowled = d["balls"]
    overs = balls_bowled // 6
    eco = (d["runs"] / (balls_bowled / 6)) if balls_bowled else 0
    print(f"{b}: W:{d['wkts']} R:{d['runs']} Eco:{eco:.2f}")

# ---- FALL OF WICKETS ----
print("\nFall of Wickets:")
for fow in fall_of_wickets:
    print(fow)

# ---- PARTNERSHIPS ----
print("\nPartnerships:")
for p in partnerships:
    print(p)

# ---------- PLAYER OF THE MATCH ----------
best_player = None
best_score = -999

# batting impact
for p, d in bat_stats.items():
    score = d["runs"] + d["4s"]*2 + d["6s"]*3
    if score > best_score:
        best_score = score
        best_player = p

# bowling impact
for b, d in bowl_stats.items():
    score = d["wkts"]*25 - d["runs"]
    if score > best_score:
        best_score = score
        best_player = b

print(GREEN + f"\nPlayer of the Match: {best_player}" + RESET)
show_graph()

# ---------- SAVE TO FILE ----------
with open("match_stats.txt", "w", encoding="utf-8") as f:

    f.write("FULL SCORECARD\n\n")

    # BATTING
    for p, d in bat_stats.items():
        runs = d["runs"]
        balls = d["balls"]
        sr = (runs / balls * 100) if balls else 0
        f.write(f"{p}: {runs}({balls}) SR:{sr:.2f}\n")

    f.write("\nBOWLING\n")
    for b, d in bowl_stats.items():
        balls = d["balls"]
        overs = balls // 6
        eco = (d["runs"] / (balls / 6)) if balls else 0
        f.write(f"{b}: W:{d['wkts']} R:{d['runs']} Eco:{eco:.2f}\n")

    f.write("\nFall of Wickets:\n")
    for fow in fall_of_wickets:
        f.write(fow + "\n")

    f.write("\nPartnerships:\n")
    for p in partnerships:
        f.write(p + "\n")

print("\nMatch saved to 'match_stats.txt'")