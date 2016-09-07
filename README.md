# python-jsonapi-datastore

Client-side [JSON API](http://jsonapi.org) data handling made easy. This is a re-write of Lucas Hosseini's [JavaScript jsonapi-datastore](https://github.com/beauby/jsonapi-datastore/) for Python. The serialization is not included yet. If you need it feel free to open a PR or ask for it.

## Description

The [JSONAPI](http://jsonapi.org) standard is great for exchanging data (which is its purpose), but the format is not ideal to work directly within an application.
python-jsonapi-datastore is a framework-agnostic library that takes away the burden of handling [JSONAPI](http://jsonapi.org) data on the client side.

What it does:
- read JSONAPI payloads,
- rebuild the underlying data graph,
- allows you to query models and access their relationships directly,
- create new models.

What it does not do:
- make requests to your API. You design your endpoints URLs, the way you handle authentication, caching, etc. is totally up to you.

## Installing

Install python-jsonapi-datastore with `pip` as usual:

    pip install jsonapi-datastore

This library has no 3rd-party dependencies.

## Parsing data

Just call the `.sync()` method of your store.
```python
store = JsonApiDataStore()
store.sync(data)
```
This parses the data and incorporates it in the store, taking care of already existing records (by updating them) and relationships.

## Parsing with meta data

If you have meta data in your payload use the `.syncWithMeta` method of your store.
```python
store = JsonApiDataStore()
store.syncWithMeta(data)
```
This does everything that `.sync()` does, but returns an object with data and meta split.

## Retrieving models

Just call the `.find(type, id)` method of your store.
```python
article = store.find('article', 123)
```
or call the `.findAll(type)` method of your store to get all the models of that type.
```python
articles = store.findAll('article')
```
All the attributes *and* relationships are accessible through the model as object properties.
```python
print(article.author.name)
```
In case a related resource has not been fetched yet (either as a primary resource or as an included resource), the corresponding property on the model will contain only the `type` and `id` (and the `._placeHolder` property will be set to `true`). However, the models are *updated in place*, so you can fetch a related resource later, and your data will remain consistent.

## Examples

```python
# Create a store:
store = JsonApiDataStore()

# Then, given the following payload, containing two `articles`, with a related `user` who is the author of both:
payload = {
  'data': [{
    'type': 'article',
    'id': 1337,
    'attributes': {
      'title': 'Cool article'
    },
    'relationships': {
      'author': {
        'data': {
          'type': 'user',
          'id': 1
        }
      }
    }
  },
  {
    'type': 'article',
    'id': 300,
    'attributes': {
      'title': 'Even cooler article'
    },
    'relationships': {
      'author': {
        'data': {
          'type': 'user',
          'id': 1
        }
      }
    }
  }]
}

# we can sync it:
articles = store.sync(payload)

# which will return the list of synced articles.

# Later, we can retrieve one of those:
article = store.find('article', 1337)

# If the author resource has not been synced yet, we can only access its id and its type:
print(article.author)
# { id: 1, _type: 'article' }

# If we do sync the author resource later:
authorPayload = {
  'data': {
    'type': 'user',
    'id': 1,
    'attributes': {
      'name': 'Lucas'
    }
  }
}

store.sync(authorPayload)

# we can then access the author's name through our old `article` reference:
print(article.author.name)
# 'Lucas'

```

## What's missing

Currently, the store does not handle `links` attributes or resource-level or relationship-level meta.

## Contributing

Pull-requests welcome!
