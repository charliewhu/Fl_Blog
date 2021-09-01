from flask import (render_template, url_for, flash,
                   redirect, request, abort, jsonify)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.posts import posts
from flaskblog.models import Post, Comment, Like
from flaskblog.posts.forms import PostForm



@posts.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('posts/create_post.html', title='Create Post', form=form)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.title.data     = post.title
        form.content.data   = post.content

    return render_template('posts/create_post.html', title='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user != current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        user=current_user, 
        post_id=post_id)\
        .first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user=current_user, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({
        "likes": len(post.likes), 
        "liked": current_user in map(lambda x: x.user, post.likes)
    })