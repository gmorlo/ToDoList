from datetime import date

from flask import Blueprint, Flask, abort, render_template, redirect, url_for, flash
from models import *
from __init__ import db

views = Blueprint("views", __name__)


@views.route('/')
def get_all_tasks():
    result = db.session.execute(
        db.select(Task).order_by(Task.importance.desc())
    )
    tasks = result.scalars().all()
    return render_template("all-tasks.html", all_tasks=tasks)


@views.route('/new-task', methods=['GET', 'POST'])
def put_new_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            name=form.name.data,
            importance=form.importance.data,
            description=form.description.data,
            status="Open",
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('views.put_new_task'))
    return render_template("add-tasks.html", form=form)


@views.route('/mark-task-done')
def update_tasks_done():
    return render_template("all-tasks.html")


@views.route('/delete-task')
def delete_task():
    return render_template("all-tasks.html")


@views.route('/all-pending-tasks')
def get_all_pending_tasks():
    return render_template("all-pending-tasks.html")


@views.route('/all-done-tasks')
def get_all_done_tasks():
    return render_template("all-done-tasks.html")


@views.route('/update-tasks')
def update_tasks():
    return render_template("update-tasks.html")
