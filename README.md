# SDP4

[![Build Status](https://travis-ci.com/jackhorse1000/SDP4.svg?token=UM9Cz1ccfUozpwDkW8ip&branch=develop)](https://travis-ci.com/jackhorse1000/SDP4)

We are designing a robot that can climb-stairs while carrying objects.

## Git Workflow

For our project we are using the [Gitflow](http://nvie.com/posts/a-successful-git-branching-model/) workflow. Instead of a single master branch, this workflow uses two branches to record the history of the project. The master branch stores the official release history, and the develop branch serves as an integration branch for features. Each new feature should reside in its own branch, which can be pushed to the central repository for backup/collaboration. But, instead of branching off of master, feature branches use develop as their parent branch. When a feature is complete, it gets merged back into develop. Features should never interact directly with master.

<p align="center">
  <img width="600" src="images/gitflow.png" />
</p>

### Rules

* Always use `git status`.

* Perform work in a feature branch.
  _Why:_
  > Because this way all work is done in isolation on a dedicated branch rather than the main branch. It allows you to submit multiple pull requests without confusion. You can iterate without polluting the master branch with potentially unstable, unfinished code. [Read more...](https://www.atlassian.com/git/tutorials/comparing-workflows#feature-branch-workflow)
* Always use `git pull --rebase` while working in a feature branch.

  _Why:_

  > Because `git pull` (without `--rebase`) would create merge commits which only clutter up the history without providing any useful information.

* Branch out from `develop`.

  _Why:_

  > This way, you can make sure that code in master will almost always build without problems.

* Never push into `develop` or `master` branch. Make a pull request.

  _Why:_

  > It notifies team members that they have completed a feature. It also enables and enforces easy code reviews.

* Delete local and remote feature branches after merging.

  _Why:_

  > It will clutter up your list of branches with dead branches. It insures you only ever merge the branch back into (`master` or `develop`) once. Feature branches should only exist while the work is still in progress.

* Before making a pull request, make sure your feature branch builds successfully and passes all tests (We need to add test).

* Write good commit messages. Write in imperative mood style and capitalise the messages.

  > You are welcome to use `git commit` without the `-m "<message>"` flag. This will bring up a text editor (likely nano or vim so make sure you know how to use those first). You can write your short commit message on the first line and then a longer description on the next line. The longer description should explain _why_ you did what you did and should be phrased as if it was an email. Don't use this for small and obvious commits.

### Do **NOT**

* Force push (`git push -f`)
* Squash branches

### Everyday workflow

* Checkout a feature branch.
  ```sh
  git checkout <feature>
  ```
* Make changes.

  ```sh
  git add
  git commit -m "commit"
  ```

* Sync with remote to get changes you have missed.

  ```sh
  git pull --rebase
  ```

* If you have conflicts [resolve them](https://help.github.com/articles/resolving-a-merge-conflict-using-the-command-line/) and continue rebase. (Remember **not** to commit.)
  ```sh
  git add <file1> <file2> ...
  git rebase --continue
  ```
* Push your branch.
  ```sh
  git push origin <subteam-feature>
  ```

### Start a new feature

* Start a new feature branch. This should be the name of the feature you are working on.

  ```sh
  git checkout develop
  git checkout -b <feature>
  git push -u origin <feature>
  ```

### Submit completed feature

* Make a pull request and resolve conflicts.
* Pull requests will be accepted, merged and closed by a reviewer.
* Remove your local feature branch if you are done.

  ```sh
  git branch -d <feature>
  ```

