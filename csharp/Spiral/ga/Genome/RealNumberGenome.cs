using System;
using System.Collections.Generic;


namespace spiral.ga
{
    public class RealNumberGenome: Genome<float>
    {
        #region Max/Min/Padding members/properties
        private static float pad = 0.0f;
        private static float scale = 1.0f;

        public static float Scale
        {
            get { return scale; }
            set { scale = value; }
        }

        public static float Padding
        {
            get { return pad; }
            set { pad = value; }
        }
        #endregion

        
        #region Ctors/Dtors
        public RealNumberGenome()
            :base()
        {

        }

        public RealNumberGenome(int size)
            :base(size)
        {

        }

        public RealNumberGenome(int size, bool permutation)
            :base(size, permutation)
        {

        }
        #endregion

        protected override void PermutationEncoding()
        {
            bool hit = false;
            for (int i = 0; i < size; i++)
            {
                float chromo = ((float)random.NextDouble() * scale) + pad;

                if (i == 0)
                {
                    this[i] = chromo;
                }
                else
                {
                    do
                    {
                        chromo = (float)random.NextDouble();

                        for (int x = 0; x < i; x++)
                        {
                            if (this[x] == chromo)
                            {
                                hit = true;
                                break;
                            }
                        }

                        if (!hit)
                        {
                            this[i] = chromo;
                        }

                    } while (hit);
                }

                hit = false;
            }
        }

        protected override void RandomEncoding()
        {
            for (int i = 0; i < size; i++)
            {
                this[i] = (float)random.NextDouble();
            }
        }


        public override string ToString()
        {
            string str = "RealNumberGenome";
            str += base.ToString();

            return str;
        }

    }
}
