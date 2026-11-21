// Calculate the total size (in base64 characters) of the images and files
// currently attached to the input, which will be sent with the next message.
export const calcTotalFileSizeToSend = (
  base64EncodedImages: string[],
  attachedFiles: { content: string }[]
): number => {
  return (
    base64EncodedImages.reduce((total, image) => total + image.length, 0) +
    attachedFiles.reduce((total, file) => total + file.content.length, 0)
  );
};
