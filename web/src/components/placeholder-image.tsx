import Image from "next/image";

type PlaceholderImageProps = {
  title?: string;
};

export const PlaceholderImage = (props: PlaceholderImageProps) => {
  const { title = "Placeholder Image" } = props;

  return (
    <Image
      priority
      src="/placeholder.svg"
      alt={title}
      width={800}
      height={400}
      style={{ objectFit: "cover" }}
      className="aspect-video w-full object-cover"
    />
  );
};
