using UnityEngine;
using Vector3 = UnityEngine.Vector3;

namespace BertisUtils
{
    public static class VectorUtils
    {
        public static int GimmeFive()
        {
            return 5;
        }

        public static Vector3 GetVectorFromAngle(float angle)
        {
            // Returns a vector of length 1!
            // 0 <= angle <= 360
            float angleRad = angle * (Mathf.PI / 180f);
            return new Vector3(Mathf.Cos(angleRad), Mathf.Sin(angleRad));
        }

    }
}