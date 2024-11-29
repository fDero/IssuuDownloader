# IssuuDownloader

A python commandline tool to download entire batches of documents concurrently
from [issuu.com](https://issuu.com) in the form of pdf files. The downloading process of such
files relies on the web-api of [Issuu To PDF Download Tool](https://issuudownload.com).

### How can I install it?
Right now the project is not hosted on [PyPI](https://pypi.org) yet, but you can download a pip-compatible
package from the [releases section](https://github.com/fDero/IssuuDownloader/releases). Once such
package is downloaded, you can install it using either `pip` or `pipx`

If you want to build the package from source, use `hatch` (can be installed with `pip` or `pipx` itself)
to create the package locally in the `dist` folder.

```bash
$ hatch build
$ pipx install dist/*.whl
```

### How can I use it?
To download every single issuu-document from a given issuu-web-page, just run the following command:
```bash
issuudownloader -p https://issuu.com/my-target-issuu-web-page
```
This will itself download every document on that page. It could be a stack-page, an author/uploader-user-profile
or even the home-screen. It's important to respect the following rules:

| URL Format                        | Is it valid? |
|-----------------------------------|--------------|
| https://issuu.com/something       | Yes          |
| https://www.issuu.com/something   | Yes          |
| https://issuu.com/something/      | No           |
| https://www.issuu.com/something/  | No           |
| https://issuu.com/something/1     | No           |
| https://www.issuu.com/something/1 | No           |

You can set the number of threads used during download with the `-t <number-of-threads>` option (default is `3`).
You can set the output directory (where downloaded files must go) with the `-d <download-dir-path>` option.
You can set the path to a log file with the `-l <log-file-path>` option (default is `./issuu-download.log`).

### Why Issuu-Downloader?
I developed this thing as a side-project after a friend of mine told me it was extremely time-consuming to
download every single music-score manually from pages like [scores-on-demand](https://issuu.com/scoresondemand)
and [di-blassio](https://issuu.com/diblassio). I decided to automate the process for him, doing nothing more
than exploiting existing web-APIs and creating this simple python package.