from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import cache
from app import db
from app.models import Post
from app.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        user_post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(user_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template(
        'create_post.html',
        title='New Post',
        form=form,
        legend='New Post'
    )


@posts.route('/post/<int:post_id>')
@cache.memoize(timeout=60)
def post(post_id):
    user_post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=user_post.title, post=user_post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    user_post = Post.query.get_or_404(post_id)
    if user_post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        user_post.title = form.title.data
        user_post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=user_post.id))
    elif request.method == 'GET':
        form.title.data = user_post.title
        form.content.data = user_post.content
    return render_template(
        'create_post.html',
        title='Update Post',
        form=form,
        legend='Update Post'
    )


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    user_post = Post.query.get_or_404(post_id)
    if user_post.author != current_user:
        abort(403)
    db.session.delete(user_post)
    db.session.commit()
    flash('Post has been deleted', 'success')

    return redirect(url_for('main.home'))
