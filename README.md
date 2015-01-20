# Wikidata → Virtuoso

This fully automated tool downloads and processes a [Wikidata RDF dump](https://tools.wmflabs.org/wikidata-exports/rdf/) (currently 2015-01-05), imports it into a [Virtuoso Open-Source Edition](https://github.com/openlink/virtuoso-opensource) quad store, and makes the Linked Data available via Virtuoso's built-in SPARQL endpoint.


## Prerequisites

* A Linux server ([CoreOS](https://coreos.com/), [Ubuntu](http://www.ubuntu.com/), …)
* [Docker](https://www.docker.com/)
* 4GB free memory
* ~20GB free storage
* Swap file or partition strongly recommended


## Setup

```
git clone https://github.com/patrickhoefler/wikidata-virtuoso
cd wikidata-virtuoso
./setup.sh
```

After this, no manual intervention is necessary.
However, please be patient since downloading, processing, and importing of the data will take a few hours.
The setup script will keep you informed throughout the setup.

## License

[MIT](LICENSE.txt)
