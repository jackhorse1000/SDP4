const fs = require("fs");
const http = require("http");
const path = require("path");
const url = require("url");

const mimeTypes = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
  ".png": "image/png",
  ".jpg": "image/jpg",
};

module.exports = dir => (request, response) => {
  const requestUrl = url.parse(request.url || "");
  const filePath = path.join(dir, !requestUrl.pathname || requestUrl.pathname === "/"
    ? "index.html"
    : requestUrl.pathname);

  const extname = String(path.extname(filePath)).toLowerCase();
  const mime = mimeTypes[extname];

  if (!mime) {
    fs.readFile(path.join(dir, "404.html"), { encoding: "utf-8" }, (_error, contents) => {
      response.writeHead(404, { "Content-Type": "text/html" });
      response.end(contents, "utf-8");
    });
    return;
  }

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === "ENOENT") {
        fs.readFile(path.join(dir, "404.html"), { encoding: "utf-8" }, (_error, contents) => {
          response.writeHead(404, { "Content-Type": "text/html" });
          response.end(contents, "utf-8");
        });
      } else {
        response.writeHead(500);
        response.end("Sorry, check with the site admin for error: " + error.code + " ..\n");
        response.end();
      }
    } else {
      response.writeHead(200, { "Content-Type": mime });
      response.end(content, "utf-8");
    }
  });
};
