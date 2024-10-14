from datetime import date
from flask_login import login_required, current_user
from flask import Blueprint, Flask, abort, render_template, redirect, url_for, flash
from models import *
from __init__ import db

views = Blueprint("views", __name__)


@views.route('/')
@login_required
def get_all_tasks():
    tasks = Task.query.filter_by(
        user_id=current_user.id).order_by(Task.importance.desc()).all()

    return render_template("all-tasks.html", all_tasks=tasks)


@views.route('/new-task', methods=['GET', 'POST'])
@login_required
def put_new_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            name=form.name.data,
            importance=form.importance.data,
            description=form.description.data,
            status="Open",
            date=date.today().strftime("%B %d, %Y"),
            user_id = current_user.id
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('views.put_new_task'))
    return render_template("add-tasks.html", form=form)


@views.route('/update-task-done/<int:task_id>')
@login_required
def update_tasks_done(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        abort(404)

    task.status = "Done"

    db.session.commit()

    flash("Task marked as done!", "success")
    return redirect(url_for('views.get_all_tasks'))


@views.route('/delete-task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        abort(404)

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully!", "success")
    return redirect(url_for('views.get_all_tasks'))


@views.route('/all-pending-tasks')
@login_required
def get_all_pending_tasks():
    tasks = Task.query.filter_by(
        user_id=current_user.id,
        status="Open").order_by(Task.importance.desc()).all()

    return render_template("all-pending-tasks.html", all_tasks=tasks)


@views.route('/all-done-tasks')
@login_required
def get_all_done_tasks():
    tasks = Task.query.filter_by(
        user_id=current_user.id,
        status="Done").order_by(Task.importance.desc()).all()

    return render_template("all-done-tasks.html", all_tasks=tasks)


@views.route('/update-task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_tasks(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        abort(404)

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.name = form.name.data
        task.importance = form.importance.data
        task.description = form.description.data

        db.session.commit()

        flash("Task updated successfully!", "success")
        return redirect(url_for('views.get_all_tasks'))

    return render_template("update-tasks.html", form=form)
