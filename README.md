# Scoremodel

[![Build Status](https://travis-ci.org/PACKED-vzw/scoremodel.svg?branch=master)](https://travis-ci.org/PACKED-vzw/scoremodel)

The Scoremodel ([www.scoremodel.org](http://www.scoremodel.org)) is a website where digital preservation managers can score how well the digital preservation initiatives of their institute perform. The application consists of a wizard where the user answers questions and is scored based on their answer. At the end, remedies and actions are also proposed for the questions with a low score.

## Installation
See the `INSTALL.md` file for installation instructions.

## Usage
The scoremodel application is completely multilingual. Both content and user interface are available in multiple languages, and while the user interface will fall back to English if it can't find a string in a specific language, the content will not. If content is not available for the selected language, a _404 Not Found_ will be generated.

### Administrative interface
The administrative interface is only available to administrators at `/admin`.

#### Reports
Reports are language-specific wizards consisting of sections, consisting themselves of questions. Sections and questions are answered by users in the order they are defined. Multiple reports can be created, and users can choose which one they want to use.

It is possible to drag and drop sections to change the order. The same can be done with questions, but only inside the section they are in. Changes are not permanent until the _Save_ button is clicked.

##### Sections
Sections have a title and an optional context. Markdown syntax can be used in the context field. You can provide a weight for the section as well. This is used to determine the _Top 5 actions_ on the `/summary` page (see below).

Questions are defined per section.

##### Questions
Questions have a weight, a question, a risk factor and one or more potential answers (from the _Generic answers_ list). Optionally, an example, context, list of risks and list of actions can be provided. You may use Markdown syntax in the optional fields. Note that the _Risks_ and _Example_ fields are currently not displayed.

##### Benchmarks
On the `/admin/reports` page, you can also add or modify a benchmark per report. A benchmark translates a standard for digital preservation (e.g. DSA) into the questions and answers of the report and gives an indications to users of the tool whether they conform to the standard or not. The comparison is shown on the `/summary` and `/full` pages.

For every question, you select the appropriate answer or exclude it from the benchmark.

#### Pages
Pages are linked to `menu_link`s, which correspond to the links in the top menu on the public interface. The `menu_link`s are created by the setup script and cannot be altered. There can be only one page per link per language. For the content of the page, you can use Markdown syntax.

#### Documents
Documents are files that appear on the `/documents` page. They are, as always, language-specific. Documents have a name and description as well as a attached file. They can be used to upload reference material (e.g. the standards used to create the benchmarks).

#### Users
Users can self-register, but they can also be created using the admnistrative interface. It is only the users which have the `administrator` role who can create users and assign them roles (either `administrator` or `public` (default)). You can also change the password of users in this form.

#### Generic keys
Some lists consist of generic keys (i.e. answers and risk factors in the report generation form and organisation types in the user registration form). These can be added and modified on their respective pages. A list must be created before you can create reports and register users. Note that the keys are language-specific.

* _Generic answers_ - Every answer has an answer key (e.g. "Yes" or "No") and a value (as an integer). The value of the answer is multiplied with the weight of the question and the weight of the risk factor to get the score for the selected answer on the selected question. The list is sitewide; you can't specify a custom list for a specific question.
* _Generic risk factors_ - Has a risk factor key and a value. Works the same as a _Generic answer_.
* _Generic organisation types_ - A simple list without side-effects. Used by users wanting to register.

### Scoremodel
The application itself is relatively simple. You can select a report template (created in the administrative interface), give your report a name and start the wizard (note that report templates are language specific).

Continuing a report is also possible.

Reports are completed section by section. It is not possible to "skip" a section, allthough you are not required to answer every question.

#### Scoring
At the bottom of each section, you can find your score for the section.

The score is computed as follows:

```
weight of the question * value of the risk factor * value of the selected answer
```

The score is then converted to a number /100.

#### Results
The results consist of two pages, a summary (`/summary`) and a full report (`/check` or `/full`). Both pages can be printed.

* _Summary_: contains some metadata, a graph of your scores as well as a comparison with all the attached benchmarks, and a top 5 of most important actions to take (computed by taking `maximum value of a question * weight of the section` for every question the value of your answer is not equal to the maximum value for that question).
* _Full_: also contains the metadata and the graph, but includes all the questions, with both your answer and the benchmark answers, and actions you can take for every question to remedy the defects.

## Contribute
The application is created and maintained by [PACKED vzw](http://www.packed.be).
