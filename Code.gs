/**
 * EHEPS International Organization - Workspace AI Extension
 * Primary Endpoint: https://eheps-ai-engine-xxxxxx.a.run.app
 */

const API_ENDPOINT = "https://eheps-ai-engine-xxxxxx.a.run.app/api/v1";

/**
 * Contextual Trigger for Gmail messages
 */
function onGmailMessageOpen(e) {
  const messageId = e.gmail.messageId;
  const card = CardService.newCardBuilder();
  card.setHeader(CardService.newCardHeader().setTitle("EHEPS AI Assistant"));

  const section = CardService.newCardSection()
    .addWidget(CardService.newTextParagraph().setText("Analyze field reports, grant RFPs, or translate to Dari/Pashto."))
    .addWidget(
      CardService.newSelectionInput()
        .setType(CardService.SelectionInputType.DROPDOWN)
        .setFieldName("action_type")
        .setTitle("Select Action")
        .addItem("Multilingual Summary (Dari/Pashto/EN)", "multilingual_summary", true)
        .addItem("Grant RFP Compliance Check", "grant_check", false)
        .addItem("Humanitarian Need Extraction", "humanitarian_extract", false)
    )
    .addWidget(
      CardService.newButtonSet().addButton(
        CardService.newTextButton()
          .setText("Run AI Analysis")
          .setOnClickAction(CardService.newAction().setFunctionName("handleAIExecution").setParameters({ messageId: messageId }))
      )
    );

  card.addSection(section);
  return [card.build()];
}

/**
 * Action Handler that communicates with the Cloud Run Backend
 */
function handleAIExecution(e) {
  const messageId = e.parameters.messageId;
  const formInputs = e.formInputs;
  const actionType = formInputs.action_type[0];

  // Retrieve message subject and body safely
  const message = GmailApp.getMessageById(messageId);
  const bodyContent = message.getPlainBody();

  const payload = {
    action: actionType,
    text: bodyContent.substring(0, 15000), // Enforce token threshold
    source_email: "executive@eheps.com"
  };

  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_ENDPOINT + "/process", options);
    const result = JSON.parse(response.getContentText());

    const resultCard = CardService.newCardBuilder();
    resultCard.setHeader(CardService.newCardHeader().setTitle("AI Analysis Result"));
    
    const resultSection = CardService.newCardSection()
      .addWidget(CardService.newTextParagraph().setText(result.output || "No output generated."));

    resultCard.addSection(resultSection);
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation().pushCard(resultCard.build()))
      .build();

  } catch (err) {
    const errorCard = CardService.newCardBuilder()
      .setHeader(CardService.newCardHeader().setTitle("Error"))
      .addSection(CardService.newCardSection().addWidget(CardService.newTextParagraph().setText("Execution failed: " + err.message)))
      .build();

    return CardService.newActionResponseBuilder().setNavigation(CardService.newNavigation().pushCard(errorCard)).build();
  }
}
