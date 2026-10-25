from flask import Flask, render_template, request

app = Flask(__name__)


# =========================
# LINKED LIST (data structure)
# =========================
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # ----- insert -----
    def insert_beginning(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node

    def insert_end(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def insert_after(self, after_value, value):
        """Insert value after the first node holding after_value."""
        current = self.head
        while current:
            if current.value == after_value:
                node = Node(value)
                node.next = current.next
                current.next = node
                return True
            current = current.next
        return False

    # ----- remove -----
    def remove_beginning(self):
        if self.head is None:
            return None
        removed = self.head.value
        self.head = self.head.next
        return removed

    def remove_end(self):
        if self.head is None:
            return None
        if self.head.next is None:
            removed = self.head.value
            self.head = None
            return removed
        current = self.head
        while current.next.next:
            current = current.next
        removed = current.next.value
        current.next = None
        return removed

    def remove_value(self, value):
        current = self.head
        previous = None
        while current:
            if current.value == value:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    # ----- look -----
    def search(self, value):
        """Return the position (starting at 1) of value, or 0 if not found."""
        current = self.head
        position = 1
        while current:
            if current.value == value:
                return position
            current = current.next
            position += 1
        return 0

    def to_list(self):
        values = []
        current = self.head
        while current:
            values.append(current.value)
            current = current.next
        return values


LINKED_LIST = LinkedList()

# =========================
# STACK (built from nodes) + INFIX TO POSTFIX
# =========================
class Stack:
    """Stack made of nodes. The top of the stack is the head node."""

    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, value):
        node = Node(value)
        node.next = self.top
        self.top = node

    def pop(self):
        if self.top is None:
            return None
        node = self.top
        self.top = node.next
        return node.value

    def peek(self):
        return self.top.value if self.top else None

    def to_list(self):
        """Return values from bottom to top (for display)."""
        values = []
        current = self.top
        while current:
            values.append(current.value)
            current = current.next
        values.reverse()
        return values


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

# =========================
# QUEUE (built from nodes): FIFO
# =========================
class Queue:
    """Queue made of nodes. Enqueue at the rear, dequeue from the front."""

    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, value):
        node = Node(value)
        if self.rear is None:
            self.front = node
            self.rear = node
        else:
            self.rear.next = node
            self.rear = node

    def dequeue(self):
        """Remove and return the front value, or None if the queue is empty."""
        if self.front is None:
            return None
        node = self.front
        self.front = node.next
        if self.front is None:
            self.rear = None
        return node.value

    def peek(self):
        return self.front.value if self.front else None

    def size(self):
        count = 0
        current = self.front
        while current:
            count += 1
            current = current.next
        return count

    def to_list(self):
        """Return values from front to rear (for display)."""
        values = []
        current = self.front
        while current:
            values.append(current.value)
            current = current.next
        return values


QUEUE = Queue()

def tokenize(expression):
    tokens = []
    operand = ""
    for ch in expression:
        if ch.isalnum():
            operand += ch
        else:
            if operand:
                tokens.append(operand)
                operand = ""
            if ch.isspace():
                continue
            if ch in PRECEDENCE or ch in "()":
                tokens.append(ch)
            else:
                raise ValueError(f"Invalid character: '{ch}'")
    if operand:
        tokens.append(operand)
    return tokens


def infix_to_postfix(expression):
    """Returns (postfix_string, steps). Raises ValueError on bad input."""
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Please enter an expression.")

    stack = Stack()
    output = LinkedList()
    steps = []

    for token in tokens:
        if token not in PRECEDENCE and token not in "()":
            output.insert_end(token)
        elif token == "(":
            stack.push(token)
        elif token == ")":
            while not stack.is_empty() and stack.peek() != "(":
                output.insert_end(stack.pop())
            if stack.is_empty():
                raise ValueError("Mismatched parentheses.")
            stack.pop()
        else:
            while (not stack.is_empty() and stack.peek() != "("
                   and (PRECEDENCE[stack.peek()] > PRECEDENCE[token]
                        or (PRECEDENCE[stack.peek()] == PRECEDENCE[token]
                            and token != "^"))):
                output.insert_end(stack.pop())
            stack.push(token)

        steps.append({
            "token": token,
            "stack": " ".join(stack.to_list()) or "empty",
            "output": " ".join(output.to_list()) or "empty",
        })

    while not stack.is_empty():
        op = stack.pop()
        if op == "(":
            raise ValueError("Mismatched parentheses.")
        output.insert_end(op)
        steps.append({
            "token": "pop",
            "stack": " ".join(stack.to_list()) or "empty",
            "output": " ".join(output.to_list()) or "empty",
        })

    return " ".join(output.to_list()), steps

# =========================
# PERSONAL INFORMATION
# Replace these sample values with your own data.
# =========================
PROFILE = {
    "name": "Elaine Zaire S. Gonzales",
    "course": "BS Computer Engineering",
    "section": "2-3",
    "school": "Polytechnic University of the Philippines",
    "email": "gonzaleselainezaire@gmail.com",
    "location": "Antipolo City, Rizal Province, Philippines",
    "motto": "Float like a butterfly and sting like a bee",
    "about": "Enjoy your life to the fullest.",
    "skills": ["Python"],
}

# =========================
# LINK LIST
# Replace these with your own links.
# =========================
LINKS = [
    {
        "name": "GitHub",
        "url": "https://github.com/Elaine04-dsa",
        "description": "My coding projects and repositories."
    },
    {
        "name": "Facebook",
        "url": "https://www.facebook.com/eleeynnnzaire/about",
        "description": "My social profile."
    },
    {
        "name": "Instagram",
        "url": "https://www.instagram.com/eleeyynnn_/",
        "description": "My social profile."
    },
]


@app.route("/")
def index():
    return render_template("index.html", profile=PROFILE)


@app.route("/profile")
def profile():
    return render_template("profile.html", profile=PROFILE)


@app.route("/works", methods=["GET", "POST"])
def works():
    result = None

    if request.method == "POST":
        input_string = request.form.get("inputString", "")
        result = input_string.upper()

    return render_template("touppercase.html", result=result, profile=PROFILE)


# =========================
# AREA OF CIRCLE
# =========================
@app.route("/works/area/circle", methods=["GET", "POST"])
def acircle():
    result = None
    error = None

    if request.method == "POST":
        try:
            radius = float(request.form.get("radius", ""))
            if radius < 0:
                raise ValueError
            result = 3.141592653589793 * radius * radius
        except ValueError:
            error = "Please enter a valid non-negative number."

    return render_template(
        "circle.html",
        result=result,
        error=error,
        profile=PROFILE
    )


# =========================
# AREA OF TRIANGLE
# =========================
@app.route("/works/area/triangle", methods=["GET", "POST"])
def atriangle():
    result = None
    error = None

    if request.method == "POST":
        try:
            base = float(request.form.get("base", ""))
            height = float(request.form.get("height", ""))

            if base < 0 or height < 0:
                raise ValueError

            result = 0.5 * base * height
        except ValueError:
            error = "Please enter valid non-negative numbers."

    return render_template(
        "triangle.html",
        result=result,
        error=error,
        profile=PROFILE
    )


# =========================
# CONTACT
# =========================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False

    if request.method == "POST":
        submitted = True

    return render_template(
        "contact.html",
        profile=PROFILE,
        submitted=submitted
    )


# =========================
# LINK LIST
# =========================
@app.route("/links")
def links():
    return render_template(
        "links.html",
        profile=PROFILE,
        links=LINKS
    )


# =========================
# LINKED LIST PAGE
# =========================
@app.route("/linked-list", methods=["GET", "POST"])
def linked_list():
    message = None

    if request.method == "POST":
        action = request.form.get("action", "")
        value = request.form.get("value", "").strip()
        after = request.form.get("after", "").strip()

        needs_value = ["insert_beginning", "insert_end", "insert_after",
                       "remove_value", "search"]

        if action in needs_value and not value:
            message = "Please enter a value."
        elif action == "insert_beginning":
            LINKED_LIST.insert_beginning(value)
            message = f"Inserted '{value}' at the beginning."
        elif action == "insert_end":
            LINKED_LIST.insert_end(value)
            message = f"Inserted '{value}' at the end."
        elif action == "insert_after":
            if not after:
                message = "Please enter the existing node value in 'After node'."
            elif LINKED_LIST.insert_after(after, value):
                message = f"Inserted '{value}' after '{after}'."
            else:
                message = f"Node '{after}' was not found."
        elif action == "remove_beginning":
            removed = LINKED_LIST.remove_beginning()
            message = (f"Removed '{removed}' from the beginning."
                       if removed is not None else "The list is empty.")
        elif action == "remove_end":
            removed = LINKED_LIST.remove_end()
            message = (f"Removed '{removed}' from the end."
                       if removed is not None else "The list is empty.")
        elif action == "remove_value":
            if LINKED_LIST.remove_value(value):
                message = f"Removed '{value}'."
            else:
                message = f"'{value}' was not found."
        elif action == "search":
            position = LINKED_LIST.search(value)
            if position:
                message = f"'{value}' found at position {position}."
            else:
                message = f"'{value}' was not found."
        elif action == "print":
            items = LINKED_LIST.to_list()
            if items:
                message = " -> ".join(items) + " -> None"
            else:
                message = "The list is empty."

    return render_template(
        "linked_list.html",
        profile=PROFILE,
        nodes=LINKED_LIST.to_list(),
        message=message
    )

# =========================
# QUEUE PAGE
# =========================
@app.route("/queue", methods=["GET", "POST"])
def queue_page():
    message = None

    if request.method == "POST":
        action = request.form.get("action", "")
        value = request.form.get("value", "").strip()

        if action == "enqueue":
            if not value:
                message = "Please enter a value."
            else:
                QUEUE.enqueue(value)
                message = f"Enqueued '{value}' at the rear."
        elif action == "dequeue":
            removed = QUEUE.dequeue()
            message = (f"Dequeued '{removed}' from the front."
                       if removed is not None else "The queue is empty.")
        elif action == "peek":
            front = QUEUE.peek()
            message = (f"Front of the queue: '{front}'."
                       if front is not None else "The queue is empty.")
        elif action == "print":
            items = QUEUE.to_list()
            if items:
                message = "Front -> " + " -> ".join(items) + " <- Rear"
            else:
                message = "The queue is empty."

    return render_template(
        "queue.html",
        profile=PROFILE,
        items=QUEUE.to_list(),
        size=QUEUE.size(),
        message=message
    )

# =========================
# INFIX TO POSTFIX PAGE
# =========================
@app.route("/works/infix-postfix", methods=["GET", "POST"])
def infix_postfix():
    expression = ""
    result = None
    error = None
    steps = []

    if request.method == "POST":
        expression = request.form.get("expression", "").strip()
        try:
            result, steps = infix_to_postfix(expression)
        except ValueError as e:
            error = str(e)

    return render_template(
        "infix_postfix.html",
        profile=PROFILE,
        expression=expression,
        result=result,
        error=error,
        steps=steps
    )

# =========================
# RUN THE APP (must stay at the very bottom)
# =========================
if __name__ == "__main__":
    app.run(debug=True)
