# IssuuDownloader

A python commandline tool to download entire batches of documents concurrently
from [issuu.com](https://issuu.com) in the form of pdf files. The downloading process of such
files relies on the web-api of [Issuu To PDF Download Tool](https://issuudownload.com).

### Why IssuuDownloader?
I developed this thing as a side-project after a friend of mine told me it was extremely time-consuming to
download every single music-score manually from pages like [scores-on-demand](https://issuu.com/scoresondemand)
and [diblassio](https://issuu.com/diblassio). I decided to automate the process for him, doing nothing more
than exploiting existing web-APIs and creating this simple python package.

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
To download every single issuu-document from a given issuu-repository (every web-page 
with issuu-documents in it is considered a repository, it can be an account-profile, 
or a stack web-page). When the repository is displayed as paginated in the browser, IssuuDownloader 
will download documents from all the pages of the repository.
```bash
issuudownloader -r https://issuu.com/my-target-issuu-web-page
```
This will itself download every document on that page. It could be a stack-page, an author/uploader-user-profile
or even the home-screen. It's important to respect the following rules:

<table align="center">
  <tr>
    <th>URL Format</th>
    <th>Is it valid?</th>
  </tr>
  <tr>
    <td>https://issuu.com/something</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>https://www.issuu.com/something</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>https://issuu.com/something/</td>
    <td>No</td>
  </tr>
  <tr>
    <td>https://www.issuu.com/something/</td>
    <td>No</td>
  </tr>
  <tr>
    <td>https://issuu.com/something/1</td>
    <td>No</td>
  </tr>
  <tr>
    <td>https://www.issuu.com/something/1</td>
    <td>No</td>
  </tr>
</table>

### Additional features
- You can set the number of threads used during download with the `-t [number(3)]` option.