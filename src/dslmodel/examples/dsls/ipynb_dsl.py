from dslmodel import DSLModel
from typing import List, Optional, Union
from pydantic import Field


# Notebook metadata model
class NotebookMetadataModel(DSLModel):
    kernelspec: dict = Field(..., description="Information about the notebook's kernel.")
    language_info: dict = Field(..., description="Information about the notebook's programming language.")


# Notebook output model for code cells
class NotebookOutputModel(DSLModel):
    output_type: str = Field(..., description="The type of the output (e.g., stream, display_data, error).")
    text: Optional[List[str]] = Field(None, description="Text output for streams or errors.")
    data: Optional[dict] = Field(None, description="Data output (e.g., images, JSON).")
    name: Optional[str] = Field(None, description="For stream output, the name (e.g., 'stdout', 'stderr').")
    execution_count: Optional[int] = Field(None, description="Execution count if relevant.")


# Base model for a notebook cell
class NotebookCellModel(DSLModel):
    cell_type: str = Field(..., description="The type of the cell (e.g., code, markdown, raw).")
    metadata: Optional[dict] = Field({}, description="Cell-specific metadata.")


# Code cell model
class NotebookCodeCellModel(NotebookCellModel):
    cell_type: str = "code"
    source: List[str] = Field(..., description="The source code inside the code cell.")
    execution_count: Optional[int] = Field(None, description="The execution count of the cell.")
    outputs: Optional[List[NotebookOutputModel]] = Field(None, description="Outputs produced by this code cell.")

    @classmethod
    def from_prompt(cls, prompt: str) -> "NotebookCodeCellModel":
        prompt = f"{prompt}.\n\nBest practice IPython notebook code cell formatting. " \
                 "Provide implementation if unsure."
        return super().from_prompt(prompt)


# Markdown cell model
class NotebookMarkdownCellModel(NotebookCellModel):
    cell_type: str = "markdown"
    source: List[str] = Field(..., description="Markdown text inside the cell.")


# Raw cell model
class NotebookRawCellModel(NotebookCellModel):
    cell_type: str = "raw"
    source: List[str] = Field(..., description="Raw content inside the cell.")


# Root model for the entire notebook file
class NotebookFileModel(DSLModel):
    metadata: NotebookMetadataModel
    cells: List[Union[NotebookCodeCellModel, NotebookMarkdownCellModel, NotebookRawCellModel]]

    @classmethod
    def from_ipynb_file(cls, file_path: str) -> "NotebookFileModel":
        return cls.load(file_path, file_format="json")

    def to_ipynb_file(self, file_path: str) -> None:
        self.save(file_path, file_format="json")


def main():
    """Main function"""
    from dslmodel import init_lm, init_instant, init_text
    init_text()
    elementary_cellular_automaton2 = NotebookCodeCellModel.from_prompt(
        "A code cell that implements the elementary cellular automaton rule 30.")
    print(elementary_cellular_automaton2)


if __name__ == '__main__':
    main()
