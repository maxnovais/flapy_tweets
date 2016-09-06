# coding: utf-8
from flask import Flask, render_template, flash
from flask_wtf import Form
from wtforms.fields import StringField, SelectField
from twitter import Api
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.debug = app.config['DEBUG']


@app.route('/', methods=['GET', 'POST'])
def tweets():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        screen_name = search_form.screen_name.data
        limit = search_form.amount.data or 30
        if screen_name:
            tweets = get_tweets(screen_name=screen_name, limit=limit)
            return render_template('list.html', tweets=tweets, screen_name=screen_name)
        else:
            flash('Nome de usuário é obrigatório', category='danger')
    return render_template('index.html', form=search_form)


def get_tweets(screen_name, limit):
    api = Api(consumer_key=app.config['CONSUMER_KEY'],
              consumer_secret=app.config['CONSUMER_SECRET'],
              access_token_key=app.config['ACCESS_TOKEN_KEY'],
              access_token_secret=app.config['ACCESS_TOKEN_SECRET'])
    api.VerifyCredentials()
    tweets = api.GetUserTimeline(screen_name=screen_name, count=limit)
    for tweet in tweets:
        tweet.url = 'https://twitter.com/{}/statuses/{}'.format(screen_name, tweet.id)
    return tweets


class SearchForm(Form):
    screen_name = StringField('Nome de usuário')
    amount = SelectField('Quantidade', choices=[('0', 'Qtd'), ('30', '30'), ('50', '50'), ('100', '100')])


if __name__ == '__main__':
    app.run()
