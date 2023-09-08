import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import boto3
import pyttsx3
import os
import speech_recognition as sr
from functools import partial

# Define the function to open applications


def open_app(command):
    if (
        ("GOOGLE" in command)
        or ("SEARCH" in command)
        or ("WEB BROWSER" in command)
        or ("CHROME" in command)
        or ("BROWSER" in command)
    ):
        os.system("start chrome")

    elif ("MSEDGE" in command) or ("EDGE" in command):
        os.system("start msedge")

    elif (
        ("NOTE" in command)
        or ("NOTES" in command)
        or ("NOTEPAD" in command)
        or ("EDITOR" in command)
    ):
        os.system("Notepad")

    elif ("VLCPLAYER" in command) or ("VIDEO PLAYER" in command):
        os.system("start VLC")

    elif (
        ("WINDOWSPLAYER" in command)
        or ("PLAYER" in command)
        or ("MEDIA PLAYER" in command)
    ):
        os.system("start wmplayer")

    elif ("PAINT" in command) or ("DRAW" in command) or ("MSPAINT" in command):
        os.system("mspaint")

    elif ("CALCULATOR" in command) or ("CALCI" in command) or ("CALC" in command):
        os.system("calc")

    elif ("FILE EXPLORER" in command) or ("THIS PC" in command) or ("FILES" in command):
        os.system("start explorer")

    elif ("CALENDER" in command) or ("DATE" in command) or ("DATES" in command):
        os.system("start outlookcal:")

    elif ("TERMINAL" in command) or ("COMMAND LINE" in command) or ("ROOT" in command):
        os.system("start cmd")

    elif ("CONTROL PANEL" in command) or ("CONTROL" in command):
        os.system("start control")

    elif ("WORD" in command) or ("MSWORD" in command) or ("WINWORD" in command):
        os.system("start winword")

    elif ("EXCEL" in command) or ("MSEXCEL" in command) or ("SHEET" in command):
        os.system("start excel")

    elif ("POWERPOINT" in command) or ("MSPOWERPOINT" in command) or ("PPT" in command):
        os.system("start powerpnt")

    elif ("ACCESS" in command) or ("MSACCESS" in command):
        os.system("start msaccess")

    elif (
        ("TASK MANAGER" in command)
        or ("TASK" in command)
        or ("PROCESS" in command)
        or ("PROCESSES" in command)
    ):
        os.system("start taskmgr")

    elif ("FORMAT" in command) or ("CLEANUP" in command):
        os.system("start cleanmgr")

    elif ("SETTINGS" in command) or ("MSSETTINGS") in command:
        os.system("start ms-settings:")

    elif ("STORE" in command) or ("MSSTORE" in command) or ("SOFTWARES" in command):
        os.system("start ms-windows-store:")

    elif ("ONENOTE" in command) or ("MSONENOTE" in command):
        os.system("start onenote")

    elif (
        ("EXIT" in command)
        or ("QUIT" in command)
        or ("CLOSE" in command)
        or ("0" in command)
    ):
        root.destroy()


# Define the function to process user input


def process_command(output_text, command_type, command_text):
    inp_type = command_type.get().upper()
    command = command_text.get("1.0", tk.END).strip().upper()

    if inp_type == "WRITE":
        if command:
            output_text.insert(tk.END, f"Processing written command: {command}\n")
            open_app(command)
            output_text.insert(tk.END, f"Opening: {command}\n\n")
    elif inp_type == "SPEAK":
        rec = sr.Recognizer()
        with sr.Microphone() as mic:
            output_text.insert(tk.END, "Speak:\n")
            output_text.update()
            audio = rec.listen(mic, timeout=2, phrase_time_limit=4)
            try:
                spoken_command = rec.recognize_google(audio).upper()
                output_text.insert(tk.END, f"You said: {spoken_command}\n")
                open_app(spoken_command)
                output_text.insert(tk.END, f"Opening: {spoken_command}\n\n")
            except Exception as err:
                output_text.insert(tk.END, f"Error: {err}\n\n")
    else:
        output_text.insert(tk.END, "Invalid input\n\n")

    command_text.delete("1.0", tk.END)


def create_ec2_instance(output_text):
    ec2_client = boto3.client(
        "ec2", region_name="ap-south-1"
    )  # Change the region as needed

    instance_type = simpledialog.askstring(
        "Create EC2 Instance", "Enter instance type (e.g., t2.micro):"
    )
    ami_id = simpledialog.askstring(
        "Create EC2 Instance", "Enter AMI ID (e.g., ami-0c55b159cbfafe1f0):"
    )

    if instance_type and ami_id:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
        )
        output_text.insert(tk.END, "EC2 instance created successfully!\n\n")


def create_s3_bucket(output_text):
    s3_client = boto3.client("s3", region_name="ap-south-1")

    bucket_name = simpledialog.askstring("Create S3 Bucket", "Enter the bucket name:")

    if bucket_name:
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "ap-south-1"},
        )
        output_text.insert(
            tk.END, f"S3 bucket '{bucket_name}' created successfully!\n\n"
        )


def list_ec2_instances(output_text):
    ec2_client = boto3.client(
        "ec2", region_name="ap-south-1"
    )  # Change the region as needed

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Listing EC2 instances...\n")

    response = ec2_client.describe_instances()

    instances_info = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            state = instance["State"]["Name"]
            instances_info.append(
                f"Instance ID: {instance_id}, Instance Type: {instance_type}, State: {state}"
            )

    instances_text = "\n".join(instances_info)
    output_text.insert(tk.END, instances_text + "\n\n")


def list_s3_buckets(output_text):
    s3_client = boto3.client("s3")

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Listing S3 buckets...\n")

    response = s3_client.list_buckets()

    buckets_info = [bucket["Name"] for bucket in response["Buckets"]]
    buckets_text = "\n".join(buckets_info)
    output_text.insert(tk.END, buckets_text + "\n\n")


def create_sns_topic(output_text):
    sns_client = boto3.client("sns")

    topic_name = simpledialog.askstring("Create SNS Topic", "Enter the SNS topic name:")

    if topic_name:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response["TopicArn"]
        output_text.insert(
            tk.END, f"SNS topic '{topic_name}' created with ARN: {topic_arn}\n\n"
        )


def list_sns_topics(output_text):
    sns_client = boto3.client("sns")

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Listing SNS topics...\n")

    response = sns_client.list_topics()

    topics_info = [topic["TopicArn"] for topic in response["Topics"]]
    topics_text = "\n".join(topics_info)
    output_text.insert(tk.END, topics_text + "\n\n")


def create_iam_user(output_text):
    iam_client = boto3.client("iam")

    user_name = simpledialog.askstring("Create IAM User", "Enter the IAM user name:")

    if user_name:
        response = iam_client.create_user(UserName=user_name)
        output_text.insert(tk.END, f"IAM user '{user_name}' created successfully!\n\n")


def create_lambda_function(output_text):
    lambda_client = boto3.client("lambda")

    function_name = simpledialog.askstring(
        "Create Lambda Function", "Enter the Lambda function name:"
    )
    role_arn = simpledialog.askstring(
        "Create Lambda Function", "Enter the IAM role ARN for the Lambda function:"
    )
    handler = simpledialog.askstring(
        "Create Lambda Function",
        "Enter the Lambda function handler (e.g., lambda_function.handler):",
    )
    runtime = simpledialog.askstring(
        "Create Lambda Function", "Enter the runtime (e.g., python3.8):"
    )

    file_path = filedialog.askopenfilename(
        title="Select Lambda Deployment Package (.zip)",
        filetypes=[("ZIP files", "*.zip")],
    )

    if function_name and role_arn and handler and runtime and file_path:
        with open(file_path, "rb") as file:
            code_content = file.read()

        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler,
            Code={"ZipFile": code_content},
        )

        function_arn = response["FunctionArn"]
        output_text.insert(
            tk.END,
            f"Lambda function '{function_name}' created with ARN: {function_arn}\n\n",
        )


def list_lambda_functions(output_text):
    lambda_client = boto3.client("lambda")

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Listing Lambda functions...\n")

    response = lambda_client.list_functions()

    functions_info = [function["FunctionName"] for function in response["Functions"]]
    functions_text = "\n".join(functions_info)
    output_text.insert(tk.END, functions_text + "\n\n")


def exit_app():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()


# Define the main function that creates the combined GUI


##################################################################################
def main():
    root = tk.Tk()
    root.title("Combined Chatbot and AWS Services GUI")

    # Create a frame for AWS actions
    action_frame = tk.Frame(root)
    action_frame.pack(padx=20, pady=20)

    # Create buttons for different AWS actions
    create_ec2_button = tk.Button(
        action_frame, text="Create EC2 Instance", command=create_ec2_instance
    )
    create_s3_button = tk.Button(
        action_frame, text="Create S3 Bucket", command=create_s3_bucket
    )
    list_ec2_button = tk.Button(
        action_frame, text="List EC2 Instances", command=lambda: list_ec2_instances
    )
    list_s3_button = tk.Button(
        action_frame, text="List S3 Buckets", command=lambda: list_s3_buckets
    )
    create_sns_button = tk.Button(
        action_frame, text="Create SNS Topic", command=create_sns_topic
    )
    list_sns_button = tk.Button(
        action_frame, text="List SNS Topics", command=list_sns_topics
    )
    create_iam_button = tk.Button(
        action_frame, text="Create IAM User", command=create_iam_user
    )
    create_lambda_button = tk.Button(
        action_frame, text="Create Lambda Function", command=create_lambda_function
    )
    list_lambda_button = tk.Button(
        action_frame, text="List Lambda Functions", command=list_lambda_functions
    )

    # Create a frame for output text
    output_frame = tk.Frame(root)
    output_frame.pack(padx=20, pady=20)

    output_text = tk.Text(output_frame, height=10, width=50)
    output_text.pack()

    # Create buttons for different AWS actions
    create_ec2_button = tk.Button(
        action_frame,
        text="Create EC2 Instance",
        command=partial(create_ec2_instance, output_text),
    )
    create_s3_button = tk.Button(
        action_frame,
        text="Create S3 Bucket",
        command=partial(create_s3_bucket, output_text),
    )
    list_ec2_button = tk.Button(
        action_frame,
        text="List EC2 Instances",
        command=partial(list_ec2_instances, output_text),
    )
    list_s3_button = tk.Button(
        action_frame,
        text="List S3 Buckets",
        command=partial(list_s3_buckets, output_text),
    )
    create_sns_button = tk.Button(
        action_frame,
        text="Create SNS Topic",
        command=partial(create_sns_topic, output_text),
    )
    list_sns_button = tk.Button(
        action_frame,
        text="List SNS Topics",
        command=partial(list_sns_topics, output_text),
    )
    create_iam_button = tk.Button(
        action_frame,
        text="Create IAM User",
        command=partial(create_iam_user, output_text),
    )
    create_lambda_button = tk.Button(
        action_frame,
        text="Create Lambda Function",
        command=partial(create_lambda_function, output_text),
    )
    list_lambda_button = tk.Button(
        action_frame,
        text="List Lambda Functions",
        command=partial(list_lambda_functions, output_text),
    )

    # Add buttons to the frame
    create_ec2_button.pack(fill=tk.X, pady=5)
    create_s3_button.pack(fill=tk.X, pady=5)
    list_ec2_button.pack(fill=tk.X, pady=5)
    list_s3_button.pack(fill=tk.X, pady=5)
    create_sns_button.pack(fill=tk.X, pady=5)
    list_sns_button.pack(fill=tk.X, pady=5)
    create_iam_button.pack(fill=tk.X, pady=5)
    create_lambda_button.pack(fill=tk.X, pady=5)
    list_lambda_button.pack(fill=tk.X, pady=5)

    # Create labels, radio buttons, text boxes, and buttons for the Chatbot GUI
    command_type_label = tk.Label(root, text="Select input type:")
    command_type_label.pack()

    command_type = tk.StringVar()
    command_type.set("WRITE")
    write_radio = tk.Radiobutton(
        root, text="Write", variable=command_type, value="WRITE"
    )
    speak_radio = tk.Radiobutton(
        root, text="Speak", variable=command_type, value="SPEAK"
    )
    write_radio.pack()
    speak_radio.pack()

    command_text_label = tk.Label(root, text="Enter command:")
    command_text_label.pack()

    command_text = tk.Text(root, height=5, width=50)
    command_text.pack()

    process_button = tk.Button(
        root,
        text="Process Command",
        command=lambda: process_command(output_text, command_type, command_text),
    )
    process_button.pack()

    root.mainloop()


if _name_ == "_main_":
    main()
