void BitsPlusFollow(int bit)
{
	CompressedFile.WriteBit(bit);
	for(; bits_to_follow > 0; bits_to_follow--)
		CompressedFile.WriteBit(!bit);
}